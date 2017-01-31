from django.db import models
from django.utils.translation import ugettext_lazy as _


class Supplier(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    phone = models.ForeignKey('workers.Phone',
                              verbose_name=_('Phone number'),
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    postcode = models.CharField(_('Postcode'), max_length=10, blank=True)
    address = models.CharField(_('Address'), max_length=100, blank=True)
    site = models.URLField(_('Internet address'), blank=True, unique=True)
    logo = models.ImageField(upload_to='suppliers/suppliers_logo', default=None, blank=True)

    def __str__(self):
        return self.name


class SupplierContact(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    surname = models.CharField(_('Surname'), max_length=43, blank=True)
    position = models.CharField(_('Position'), max_length=30, blank=True)
    phone = models.ForeignKey('workers.Phone',
                              verbose_name=_('Phone'),
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL)
    email = models.EmailField(_('Email address'), blank=True, unique=True, null=True)
    description = models.TextField(_('Additional information'), blank=True)
    employer = models.ForeignKey('Supplier',
                                 verbose_name=_('Employer'),
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.name.capitalize(), self.surname.capitalize())
