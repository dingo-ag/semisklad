from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _


class Case(models.Model):
    class CaseMountingType:
        SURFACE = 1
        PIN = 2
        OTHER = 3

        choices = (
            (SURFACE, _('Surface mounting')),
            (PIN, _('Pin assembly')),
            (OTHER, _('Other')),
        )

    name = models.CharField(_('Name'), max_length=50, unique=True)
    image = models.ImageField(_('Image'), upload_to='components/case/images', default='images/no_image.png')
    documentation = models.FileField(_('Documentation'), upload_to='components/case/documentation', blank=True)
    mounting_type = models.IntegerField(
        verbose_name=_('Mounting type'),
        choices=CaseMountingType.choices,
        default=CaseMountingType.OTHER
    )

    def __str__(self):
        return self.name


class Component(models.Model):
    class ComponentType:
        RESISTOR = 1
        CAPACITOR = 2
        INDUCTIVITY = 3
        # VARISTOR = 4
        # THERMISTOR = 5
        # FUSE = 6
        # ARRESTER = 7
        # QUARTZ = 8
        # ACOUSTIC = 9
        # CORE = 10
        DIODE = 11
        SUPPRESSOR = 12
        ZENER_DIODE = 13
        # THYRISTOR = 14
        TRANSISTOR = 15
        # OPTOCOUPLER = 16
        CHIP = 17
        # CONTACT = 18
        # RELAY = 19
        # WIRE = 20
        # CONTACTOR = 21
        # RADIOATOR = 22
        BOARD_BLANK = 23
        BOARD = 24
        DEVICE = 25
        OTHER = 26

        choices = (
            (RESISTOR, _('Resistor')),
            (CAPACITOR, _('Capacitor')),
            (INDUCTIVITY, _('Inductivity')),
            (DIODE, _('Diode')),
            (SUPPRESSOR, _('Suppressor')),
            (ZENER_DIODE, _('Zener diode')),
            (TRANSISTOR, _('Transistor')),
            (CHIP, _('Chip')),
            (BOARD_BLANK, _('Blank board')),
            (BOARD, _('Board')),
            (DEVICE, _('Device')),
            (OTHER, _('Other')),
        )

    component_type = models.IntegerField(_('Type'), choices=ComponentType.choices, default=ComponentType.OTHER)
    name = models.CharField(_('Name'), max_length=30)
    value = models.CharField(_('Value'), max_length=20, default='')
    case = models.ForeignKey('Case', verbose_name=_('Case'), blank=True, null=True, on_delete=models.CASCADE)
    documentation = models.FileField(_('Documentation'), upload_to='components/documentation', blank=True)
    short_characteristic = models.TextField(_('Short Characteristic'), blank=True)
    analogue = models.ManyToManyField('self', verbose_name=_('Analogue'), blank=True)
    template = JSONField(_('Template'), blank=True, null=True)

    def __str__(self):
        return self.name
