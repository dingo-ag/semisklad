from django.contrib import admin
from .models import Worker, Phone, Recovery

admin.site.register(Worker)
admin.site.register(Phone)


@admin.register(Recovery)
class RecoveryAdmin(admin.ModelAdmin):
    list_display = ['worker', 'created', 'status']
    ordering = ['-status']
    fields = ['worker', 'code', 'status']
