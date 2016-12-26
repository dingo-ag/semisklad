from django.conf.urls import url

from apps.components import views

app_name = 'components'

urlpatterns = [
    url(r'^components/active$', views.active_components, name='active_components'),
    url(r'^new$', views.create_component, name='new_component'),
]
