from django.conf.urls import url
from .views import storage_list


urlpatterns = [
    url(r'^$', storage_list),
]
