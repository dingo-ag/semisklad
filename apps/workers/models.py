from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import WorkerManager


class Worker(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    name = models.CharField(_('First Name'), max_length=40)
    surname = models.CharField(_('Last Name'), max_length=40, blank=True)
    phone = models.ForeignKey('Phone', verbose_name=_('Phone'), blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(_('Additional information'), blank=True)
    is_admin = models.BooleanField(_('Administrator'), default=False)
    is_active = models.BooleanField(_('User is active'), default=True)

    objects = WorkerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_short_name(self):
        return self.name.capitalize()

    def get_full_name(self):
        return '%s %s' % (self.name.capitalize(), self.surname.capitalize())

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.name.capitalize()


class Phone(models.Model):
    number = models.CharField(max_length=25, verbose_name=_('Phone number'), unique=True, null=True)

    def __str__(self):
        return self.number
