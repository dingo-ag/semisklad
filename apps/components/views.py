from django.db.models import Count, Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import ListView

from apps.components.models import Component
from apps.components.forms import CreateComponentFrom


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
    return render(request, 'components/component_add.html', context)


class ComponentsList(ListView):
    template_name = 'components/components_list.html'
    context_object_name = 'components'
    paginate_by = 3
    paginate_orphans = 0
    queryset = Component.objects.all()
    #
    # def get_queryset(self):
    #     queryset = Component.objects.distinct('name', 'value', 'case')
    #     for q in queryset:
    #         q.__dict__['count'] = Component.objects.filter(name=q.name, value=q.value, case=q.case).count()
    #     return queryset
