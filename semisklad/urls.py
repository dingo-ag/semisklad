from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^components/', include('apps.components.urls')),
    url(r'^storage/', include('apps.storage.urls')),
    url(r'^suppliers/', include('apps.suppliers.urls')),
    url(r'^workers/', include('apps.workers.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.common.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
