from django.contrib import admin
from apps.components.models import Case, Component


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'short_characteristic']
    list_filter = ['component_type', 'case', 'value']

admin.site.register(Case)
# admin.site.register(Component)
