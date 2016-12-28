from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from apps.workers.models import Worker


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

        # Set the label for the "username" field.
        # UserModel = get_user_model()
        # self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        # if self.fields['email'].label is None:
        #     self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        print(email, password)

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                print(email, password)

                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.username_field.verbose_name},
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
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)
    password_confim = forms.CharField(max_length=40, widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=20)
    class Meta:
        model = Worker
        fields = ['email', 'name', 'surname', 'phone_number', 'password', 'password_confim']
        widgets = {
            'password': forms.PasswordInput,
            'password_confim': forms.PasswordInput
        }
