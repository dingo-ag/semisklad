from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.components.models import Component


@login_required()
def startpage(request):
    context = {}
    return render(request, 'index.html', context)


@login_required()
def search(request):
    query = request.GET.get('q', '')
    is_first_run = 'q' not in request.GET
    context = {
        'question': query,
        'first_run': is_first_run,
    }
    if not is_first_run:
        print(query)
        if query:
            result = Component.objects.filter(case__name__contains=query).order_by('id')
            context['components'] = result
    return render(request, 'search.html', context)
