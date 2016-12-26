from django.conf.urls import url, include
from django.contrib import admin
from semisklad.views import startpage, search
from django.conf import settings
from django.conf.urls.static import static

# from django.contrib.flatpages import views


urlpatterns = [
    url(r'^$', startpage, name='startpage'),
    url(r'^components/', include('apps.components.urls')),
    url(r'^storage/', include('apps.storage.urls')),
    url(r'^suppliers/', include('apps.suppliers.urls')),
    url(r'^workers/', include('apps.workers.urls')),
    url(r'^search/$', search, name='search'),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
