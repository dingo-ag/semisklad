from django.conf.urls import url
from .views import workers_list, WorkerRegistration, change_password
from django.contrib.auth.views import login, logout
from .forms import AuthForm
from django.contrib.auth.forms import AuthenticationForm


urlpatterns = [
    url(r'^$', workers_list),
    url(r'^registration/$', WorkerRegistration.as_view(), name='registration'),
    url(r'login/$', login, {'template_name': 'workers/login.html', 'authentication_form': AuthForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'change_password/$', change_password)
]
