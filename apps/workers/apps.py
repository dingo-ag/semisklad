from django.apps import AppConfig
from django.db.models.signals import post_save

from apps.workers.signals import worker_post_save
from django.utils.translation import ugettext_lazy as _


class WorkersConfig(AppConfig):
    name = 'apps.workers'
    verbose_name = _('Worker')

    def ready(self):
        from apps.workers.models import Worker
        post_save.connect(worker_post_save, sender=Worker)
