from django.conf.urls import url
from .views import workers_list, WorkerRegistration, ChangePassword, ForgetPassword, RestorePassword
from django.contrib.auth.views import login, logout
from .forms import AuthForm


urlpatterns = [
    url(r'^$', workers_list),
    url(r'^registration/$', WorkerRegistration.as_view(), name='registration'),
    url(r'login/$', login, {'template_name': 'workers/login.html', 'authentication_form': AuthForm, }, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'change-password/$', ChangePassword.as_view(), name='change_password'),
    url(r'forget-password/$', ForgetPassword.as_view(), name='forget_password'),
    url(r'restore-password/(?P<code>\w*)$', RestorePassword.as_view(), name='restore_password')
]
