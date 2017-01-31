from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _

# from utils.restore_password import generate_key
from utils.phone import PhoneNormalize
from apps.workers.models import Worker
from django.core.exceptions import ObjectDoesNotExist
# from django.core import validators


class AuthForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                # print(email, password)

                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class RegistrationForm(forms.Form):
    email = forms.EmailField(min_length=4)
    name = forms.CharField(min_length=2, max_length=40)
    surname = forms.CharField(min_length=2, max_length=40, required=False)
    password = forms.CharField(min_length=8, max_length=40, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=8, max_length=40, widget=forms.PasswordInput)
    phone_number = forms.CharField(min_length=8, max_length=20, required=False)

    error_messages = {
        'invalid_password': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'passwords are not equal': _("Passwords aren't equal"),
        'phone is already exist': _('Phone is already exist'),
        'this email is already exist': _('This email is already exist')
    }

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password == password_confirm:
            if validate_password(password) is not None:
                raise forms.ValidationError(
                    self.error_messages['invalid_password'],
                    code='invalid_password'
                )
            self.cleaned_data['password'] = password
        else:
            raise forms.ValidationError(
                    self.error_messages['passwords are not equal'],
                    code='passwords are not equal',
                )
        phone = self.cleaned_data.get('phone_number')
        workers = Worker.objects.select_related('phone')
        p = PhoneNormalize(phone)
        if workers.filter(phone__number__iexact=p.normalize_phone_number()):
            raise forms.ValidationError(
                self.error_messages['phone is already exist'],
                code='phone is already exist',
            )
        if workers.filter(email__iexact=self.cleaned_data.get('email')):
            raise forms.ValidationError(
                self.error_messages['this email is already exist'],
                code='this email is already exist',
            )
        self.cleaned_data['phone_number'] = p.normalize_phone_number()
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)
    old_password = forms.CharField(min_length=8, label=_('Old Password'), widget=forms.PasswordInput, strip=False)
    new_password = forms.CharField(min_length=8, label=_('New password'), widget=forms.PasswordInput, strip=False)
    new_password_confirm = forms.CharField(
        min_length=8,
        label=_('Repeat new password'),
        widget=forms.PasswordInput,
        strip=False
    )
    error_messages = {
        "Username or password is wrong": _("Username or password is wrong"),
        "New passwords don't match": _("New passwords don't match")
    }

    def clean(self, *args, **kwargs):
        try:
            user = Worker.objects.get(email=self.cleaned_data.get('email'))
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                self.error_messages["Username or password is wrong"],
                code='Username or password is wrong'
            )
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')

        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if not check_password(old_password, user.password):
            raise forms.ValidationError(
                {'old_password': self.error_messages["Old password wrong"]},
                code='invalid'
            )
        if not user:
            raise forms.ValidationError(
                self.error_messages['Username or password is wrong'],
                code='Username or password is wrong'
            )
        if new_password != new_password_confirm:
            raise forms.ValidationError(
                self.error_messages["New passwords don't match"]
            )
        return self.cleaned_data


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    error_messages = {
        'user_does_not_exist': _('Wrong user')
    }

    def clean(self):
        if not Worker.objects.filter(email=self.cleaned_data.get('email', '')).exists():
            raise forms.ValidationError(
                self.error_messages['user_does_not_exist'],
                code='Wrong user')
        return self.cleaned_data


class EnterNewPasswordForm(ChangePasswordForm):
    old_password = None

    def clean(self, *args, **kwargs):
        if not Worker.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError(
                self.error_messages["Username or password is wrong"],
                code='Username or password is wrong'
            )
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise forms.ValidationError(
                self.error_messages["New passwords don't match"]
            )
        return self.cleaned_data
