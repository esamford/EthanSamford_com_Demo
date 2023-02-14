from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    context = {}

    if not request.user.is_authenticated:
        context['projects'] = Project.objects.filter(make_public=True).order_by('-start_date')
    else:
        context['projects'] = Project.objects.order_by('-start_date')
    return render(request, 'projects.html', context=context)


def show_project(request, id):
    context = {}

    if not request.user.is_authenticated:
        context['project'] = get_object_or_404(Project, id=id, make_public=True)
    else:
        context['project'] = get_object_or_404(Project, id=id)

    return render(request, 'show_project.html', context=context)
