from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import login
from django.views.generic import CreateView, FormView
from .forms import RegistrationForm
from .models import Worker


def workers_list(request):
    return redirect('/', request)


class WorkerRegistration(FormView):
    template_name = 'workers/registration.html'
    form_class = RegistrationForm
    # model = Worker
    success_url = '/'


def change_password(request):
    pass
