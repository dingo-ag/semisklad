from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from semisklad.settings.local import HOST_NAME, HOST_PORT
from utils.mail import mailer
from utils.phone import PhoneNormalize
from apps.workers.models import Worker, Phone, Recovery
from utils.restore_password import create_code, check_code


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


class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(min_length=8, max_length=40, widget=forms.PasswordInput)
    phone_number = forms.CharField(min_length=8, max_length=25, required=False)
    error_messages = {
        'email or password already exists': _('Email or password already exists. Change them and try again'),
        'passwords are not equal': _("Passwords aren't equal"),
        'phone is already exist': _('Phone is already exist'),
    }

    class Meta:
        model = Worker
        fields = ['email', 'name', 'surname', 'password', 'password_confirm', 'phone_number']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Worker.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email or password already exists'],
                code='email or password already exists'
            )
        return email

    def clean_password_confirm(self):
        password_confirm = self.cleaned_data['password_confirm']
        if self.cleaned_data['password'] != password_confirm:
            raise forms.ValidationError(
                self.error_messages['passwords are not equal'],
                code='passwords are not equal'
            )
        return password_confirm

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        if phone_number:
            phone_number = PhoneNormalize(phone_number).normalize_phone_number()
            if Phone.objects.filter(number=phone_number).exists():
                raise forms.ValidationError(
                            self.error_messages['phone is already exist'],
                            code='phone is already exist',
                        )
            self.cleaned_data['phone_number'] = phone_number
        return phone_number

    def save(self, commit=True):
        self.cleaned_data.pop('password_confirm', '')
        phone_number = self.cleaned_data.pop('phone_number', '')
        if phone_number:
            phone = Phone.objects.create(number=phone_number)
        else:
            phone = None
        self.cleaned_data['phone'] = phone
        if commit:
            instance = Worker.objects.create_user(**self.cleaned_data)
        else:
            instance = Worker(**self.cleaned_data)
        return instance


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(label=_('Old password'), min_length=8, max_length=40, widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label=_('Password confirm'),
        min_length=8,
        max_length=40,
        widget=forms.PasswordInput
    )
    isinstance = None
    error_messages = {
        'email or password wrong': _('Email or password wrong'),
        'passwords are not equal': _("Passwords aren't equal"),
    }

    class Meta:
        model = Worker
        fields = ['email', 'old_password', 'password', 'password_confirm']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self.instance = Worker.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                self.error_messages['email or password wrong'],
                code='email or password wrong'
            )
        return email

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.instance.password):
            raise forms.ValidationError(
                self.error_messages['username or password wrong'],
                code='username or password wrong'
            )
        return old_password

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError(
                self.error_messages['passwords are not equal'],
                code='passwords are not equal'
            )
        return password_confirm

    def save(self, commit=True):
        password = self.cleaned_data['password']
        self.instance.set_password(password)
        if commit:
            instance = self.instance.save()
        else:
            instance = self.instance
        return instance


class ForgetPasswordForm(ChangePasswordForm):
    """
    "self.instance" is instance of Worker
    "instance" is instance of Recovery
    """
    old_password = None
    password_confirm = None

    class Meta:
        model = Worker
        fields = ['email']

    def save(self, commit=True):
        worker = self.instance
        code = create_code(worker.id)
        kwargs = {
            'code': code,
            'status': Recovery.Statuses.ACTIVE,
            'worker': worker,
        }
        mail_context = {
            'name': worker.name,
            'site_url': HOST_NAME + str(':' + HOST_PORT if HOST_PORT else ''),
            'code': code,
            'image_link': 'images/SOM.png'
        }
        if commit is True:
            Recovery.objects.filter(worker=self.instance).update(status=Recovery.Statuses.INACTIVE)
            instance = Recovery.objects.create(**kwargs)
            mailer(
                to=[worker.email],
                subject=HOST_NAME + ' restore password',
                context=mail_context,
                template_name='emails/restore_password.html'
            )
        else:
            instance = Recovery(**kwargs)
        return instance


class EnterNewPasswordForm(forms.ModelForm):
    changed = False

    check_email = forms.EmailField(label=_('Email'))
    new_password = forms.CharField(label=_('New password'), min_length=8, max_length=128, widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(
        label=_('New password confirm'),
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput)

    error_messages = {
        'email or restore code wrong': _('Email or restore code wrong'),
        'passwords are not equal': _('passwords are not equal'),
    }

    class Meta:
        model = Worker
        fields = ['email']  # , 'check_email', 'new_password', 'new_password_confirm']
        widgets = {
            'email': forms.HiddenInput
        }

    def clean_check_email(self):
        check_email = self.cleaned_data['check_email']
        if check_email != self.instance.email:
            raise forms.ValidationError(
                self.error_messages['email or restore code wrong'],
                code='email or restore code wrong'
            )
        return check_email

    def clean_new_password_confirm(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise forms.ValidationError(
                self.error_messages['passwords are not equal'],
                code='passwords are not equal'
            )
        return new_password_confirm

    def save(self, commit=True):
        password = self.cleaned_data.get('new_password')
        try:
            recovery = Recovery.objects.get(worker=self.instance, status=Recovery.Statuses.ACTIVE)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise Http404('Code is not valid')

        if recovery.is_active and check_code(recovery.code, self.instance.id):
            self.instance.set_password(password)
            if commit:
                self.instance.save()
                self.changed = True
            recovery.status = Recovery.Statuses.INACTIVE
            recovery.save()
            return self.instance
        else:
            raise Http404('Code is not active or wrong email')
