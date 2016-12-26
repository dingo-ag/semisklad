from django.db import models
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal


class Status(models.Model):
    class StatusSettings:
        EXPECT = 1
        ASSEMBLING = 2
        TESTING = 3
        IN_STOCK = 4
        WROTE_OFF = 5

        choices = (
            (EXPECT, _('Expecting')),
            (ASSEMBLING, _('Assembling')),
            (TESTING, _('Testing')),
            (IN_STOCK, _('In storage')),
            (WROTE_OFF, _('Wrote off'))
        )

    status = models.IntegerField(
        verbose_name=_('Status'),
        choices=StatusSettings.choices,
        default=StatusSettings.EXPECT
    )
    worker = models.ForeignKey('workers.Worker', verbose_name=_('Responsible person'), on_delete=models.CASCADE)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
    reason = models.TextField(_('Reason'), blank=True)


class Storage(models.Model):
    component = models.ForeignKey('components.Component', verbose_name=_('Component'), on_delete=models.CASCADE)
    supplier = models.ForeignKey('suppliers.Supplier', verbose_name=_('Supplier'), on_delete=models.CASCADE)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=4, default=Decimal(0))
    date_of_creation = models.DateTimeField(_('Creation Date'), auto_now_add=True)
    modified = models.DateTimeField(_('Date of modifying'), auto_now=True)
    status = models.ForeignKey('Status', verbose_name=_('Status'), on_delete=models.CASCADE)
    serial_number = models.IntegerField(_('Serial number'), unique=True, blank=True)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.component__name
