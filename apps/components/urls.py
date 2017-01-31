from django.conf.urls import url

from apps.components.views import create_component, ComponentsList

app_name = 'components'

urlpatterns = [
    url(r'^$', ComponentsList.as_view(), name='components_list'),
    url(r'^new$', create_component, name='new_component'),
]
