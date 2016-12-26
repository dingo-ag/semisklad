from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import SuppliersList, SupplierDetail


urlpatterns = [
    url(r'^$', login_required(SuppliersList.as_view()), name='suppliers-list'),
    url(r'^(?P<pk>\d+)/$', login_required(SupplierDetail.as_view()), name='supplier-detail'),
]
