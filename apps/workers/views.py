from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import login
from .forms import AuthForm


def workers_list(request):
    return redirect('/', request)


def registration(request):
    pass


def change_password(request):
    pass
