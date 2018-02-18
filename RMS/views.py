from el_pagination.decorators import page_templates
from django.db.models import Max
from project.models import Project
from django.shortcuts import render


@page_templates({
    'home/unauthorized_open_projects.html': 'unauthorized_open_projects',
    'home/unauthorized_close_projects.html': 'unauthorized_close_projects',
    'home/manager_projects.html': 'manager_projects',
    'home/developer_projects.html': 'developer_projects',
    'home/business_analyst_projects.html': 'business_analyst_projects',
    'home/system_analyst_projects.html': 'system_analyst_projects',
})
def home(request, template='home.html', extra_context=None):
    if request.user.is_authenticated():
        context = {
            'manager_projects': Project.objects.filter(status='open', member__user=request.user, member__role='manager'),
            'developer_projects': Project.objects.filter(status='open', member__user=request.user, member__role='developer'),
            'business_analyst_projects': Project.objects.filter(status='open', member__user=request.user, member__role='business_analyst'),
            'system_analyst_projects': Project.objects.filter(status='open', member__user=request.user, member__role='system_analyst'),
        }
    else:
        context = {
            'unauthorized_close_projects': Project.objects.filter(status='close').order_by('-revision_date'),
            'unauthorized_open_projects': Project.objects.filter(status='open').order_by('-revision_date'),
        }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def unauthorized_open_projects(request):
    context = {
        'unauthorized_open_projects': Project.objects.filter(status='open').order_by('-revision_date'),
    }
    return render(request, "home/unauthorized_open_projects.html", context)


def unauthorized_close_projects(request):
    context = {
        'unauthorized_close_projects': Project.objects.filter(status='close').order_by('-revision_date'),
    }
    return render(request, "home/unauthorized_close_projects.html", context)


def manager_projects(request):
    context = {
        'manager_projects': Project.objects.filter(status='open', member__user=request.user, member__role='manager'),
    }
    return render(request, "home/manager_projects.html", context)


def developer_projects(request):
    context = {
        'developer_projects': Project.objects.filter(status='open', member__user=request.user, member__role='developer'),
    }
    return render(request, "home/developer_projects.html", context)


def business_analyst_projects(request):
    context = {
        'business_analyst_projects': Project.objects.filter(status='open', member__user=request.user, member__role='business_analyst'),
    }
    return render(request, "home/business_analyst_projects.html", context)


def system_analyst_projects(request):
    context = {
        'system_analyst_projects': Project.objects.filter(status='open', member__user=request.user, member__role='system_analyst'),
    }
    return render(request, "home/system_analyst_projects.html", context)
