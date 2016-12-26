from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from apps.components.models import Component
from apps.components.forms import CreateComponentFrom


# from django.contrib.auth.models import User


def create_component(request):
    context = {}
    print(request.method, request.user, request.GET)
    if request.method == 'POST':
        form = CreateComponentFrom(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        context['form'] = CreateComponentFrom()
        if request.GET.get('q') == '!':
            raise Http404('Wrong!')
    return render(request, 'components/new_component.html', context)


def active_components(request):
    components = Component.objects.all()
    context = {
        'components': components
    }
    return render(request, 'components/components_list.html', context)
