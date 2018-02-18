from itertools import product
from string import ascii_uppercase
from django.template import RequestContext
from django.template.context_processors import csrf
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string, get_template
import reversion
import json
import re
from weasyprint import HTML
from reversion.models import Version
from .models import (Project, GroupRequirementType, GroupTask, UserCharacteristic, UserCharacteristicDictionary, Function, Member, Task, Comment, Purpose, CreationGoal, ObjectInformation, GroupRequirementTypeDictionary, GroupRequirement, Requirement, Specification)
from .forms import (MemberAddForm, GroupRequirementTypeFormSet, GroupRequirementForm, RequirementForm, GroupTaskForm, TaskForm, UserCharacteristicForm, FunctionForm, CommentForm, PurposeForm, CreationGoalForm, ObjectInformationForm, V_RequirementForm, FA_GroupRequirementForm, FA_RequirementForm, DF_GroupRequirementForm, DF_RequirementForm, SpecificationForm, RequirementFormTree)


def dashboard(request, template='project/project_list.html', extra_context=None):
    context = {
        'projects': Project.objects.filter(status='open', member__user=request.user).order_by('-creation_date'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def project_detail(request, project_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_types = GroupRequirementType.objects.filter(project=project_code, is_visible=True)
    group_tasks = GroupTask.objects.filter(project=project_code).order_by('create_time', 'symbol')
    user_characteristics = UserCharacteristic.objects.filter(project=project_code).order_by('-create_time')
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    request_user_is_manager = project.member_set.filter(user=request.user, role='manager').exists()
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    request_user_is_developer = project.member_set.filter(user=request.user, role='developer').exists()
    group_task_comment_form = CommentForm(request.POST)
    user_characteristic_comment_form = CommentForm(request.POST)
    creation_goal_comment_form = CommentForm(request.POST)
    creation_goals = CreationGoal.objects.filter(project=project_code)
    creation_goal_is_exist = CreationGoal.objects.filter(project=project_code).exists()
    purpose_comment_form = CommentForm(request.POST)
    purposes = Purpose.objects.filter(project=project_code)
    purpose_is_exist = Purpose.objects.filter(project=project_code).exists()
    object_information_comment_form = CommentForm(request.POST)
    object_information_all = ObjectInformation.objects.filter(project=project_code)
    object_information_is_exist = ObjectInformation.objects.filter(project=project_code).exists()
    member = project.member_set.get(user=request.user)
    context = {
        'project': project,
        'group_requirement_types': group_requirement_types,
        'group_tasks': group_tasks,
        'user_characteristics': user_characteristics,
        'request_user_is_manager': request_user_is_manager,
        'request_user_is_system_analyst': request_user_is_system_analyst,
        'request_user_is_business_analyst': request_user_is_business_analyst,
        'request_user_is_developer': request_user_is_developer,
        'group_task_comment_form': group_task_comment_form,
        'user_characteristic_comment_form': user_characteristic_comment_form,
        'purpose_comment_form': purpose_comment_form,
        'purposes': purposes,
        'purpose_is_exist': purpose_is_exist,
        'creation_goal_is_exist': creation_goal_is_exist,
        'creation_goals': creation_goals,
        'creation_goal_comment_form': creation_goal_comment_form,
        'object_information_all': object_information_all,
        'object_information_comment_form': object_information_comment_form,
        'object_information_is_exist': object_information_is_exist,
        'role': member.get_role_display(),
    }
    return render(request, 'project/project_detail.html', context)


def project_member_add(request, project_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    if request.method == 'POST':
        form = MemberAddForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if Member.objects.filter(user=user, project=project_code).exists():
                form.add_error('user', _('This user is already a member of the project!'))
            else:
                new_member = form.save(commit=False)
                new_member.project = project
                new_member.save()
                data['form_is_valid'] = True
                data['html_project_member'] = render_to_string('project/project_member_list.html', {'project': project})
        else:
            data['form_is_valid'] = False
    else:
        form = MemberAddForm()
    context = {'project': project, 'form': form}
    data['html_project_member_form'] = render_to_string('project/project_member_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def group_task_add(request, project_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    group_task_comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        group_task_form = GroupTaskForm(request.POST)
        if group_task_form.is_valid():
            name = group_task_form.cleaned_data['name']
            if GroupTask.objects.filter(name=name, project=project_code).exists():
                group_task_form.add_error('name', _('Group task with the same name is already exist in this project!'))
            else:
                group_task = group_task_form.save(commit=False)
                symbols = [''.join(i) for i in product(ascii_uppercase, repeat=1)] + [a + b for a, b in product(ascii_uppercase, repeat=2)]
                for symbol in symbols:
                    if not GroupTask.objects.filter(project=project_code, symbol=symbol).exists():
                        group_task.symbol = symbol
                        break
                group_task.project = project
                group_task.save()
                data['form_is_valid'] = True
                group_tasks = GroupTask.objects.filter(project=project_code).order_by('create_time')
                context = {'project': project, 'group_task': group_task, 'group_tasks': group_tasks, 'group_task_comment_form': group_task_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
                context.update(csrf(request))
                data['html_group_task'] = render_to_string('project/group_task_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        group_task_form = GroupTaskForm()
    context = {'project': project, 'group_task_form': group_task_form}
    data['html_group_task_form'] = render_to_string('project/group_task_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def group_task_edit(request, project_code, group_task_code):
    data = dict()
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    project = get_object_or_404(Project, pk=project_code)
    group_task_comment_form = CommentForm(request.POST)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        group_task_form = GroupTaskForm(request.POST, instance=group_task)
        if group_task_form.is_valid():
            group_task_form.save()
            data['form_is_valid'] = True
            group_tasks = GroupTask.objects.filter(project=project_code)
            group_task.comments.clear()
            context = {'project': project, 'group_task': group_task, 'group_tasks': group_tasks, 'group_task_comment_form': group_task_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_group_task'] = render_to_string('project/group_task_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        group_task_form = GroupTaskForm(instance=group_task)
    context = {'project': project, 'group_task': group_task, 'group_task_form': group_task_form}
    data['html_group_task_form'] = render_to_string('project/group_task_edit.html', context, request=request)
    return JsonResponse(data)


def group_task_detail(request, project_code, group_task_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    tasks = Task.objects.filter(group_task=group_task_code).order_by('create_time')
    form = CommentForm(request.POST)
    member = project.member_set.get(user=request.user)
    context = {
        'project': project,
        'group_task': group_task,
        'tasks': tasks,
        'form': form,
        'request_user_is_business_analyst': request_user_is_business_analyst,
        'role': member.get_role_display()
    }
    return render(request, 'project/group_task_detail.html', context)


def group_task_comment_add(request, project_code, group_task_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        group_task_comment_form = CommentForm(request.POST)
        if group_task_comment_form.is_valid():
            comment = group_task_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            group_task.comments.add(comment)
            data['form_is_valid'] = True
            context = {'group_task': group_task, 'request_user_is_business_analyst': request_user_is_business_analyst}
            data['html_group_task_comment'] = render_to_string('project/group_task_comment_list.html', context)
            data['html_group_task_comment_number'] = render_to_string('project/group_task_comment_number.html', {'group_task': group_task})
        else:
            data['form_is_valid'] = False
    else:
        group_task_comment_form = CommentForm()
    context = {'project': project, 'group_task': group_task, 'group_task_comment_form': group_task_comment_form}
    data['html_group_task_comment_form'] = render_to_string('project/group_task_comment_form.html', context, request=request)
    return JsonResponse(data)


def group_task_reversions(request, project_code, group_task_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    versions = Version.objects.get_for_object(group_task)
    member = project.member_set.get(user=request.user)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'group_task': group_task, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/group_task_reversions.html', context)


@reversion.create_revision()
def group_task_revert(request, project_code, group_task_code, group_task_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    revision = get_object_or_404(Version.objects.get_for_object(group_task), pk=group_task_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    group_task.comments.clear()
    return redirect('project:project_detail', project_code=project.code)


@reversion.create_revision()
def task_add(request, project_code, group_task_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    form = CommentForm(request.POST)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            name = task_form.cleaned_data['name']
            if Task.objects.filter(group_task=group_task_code, name=name).exists():
                task_form.add_error('name', _('Task with the same name is already exist in this group task!'))
            else:
                task = task_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not Task.objects.filter(group_task=group_task_code, symbol=group_task.symbol + "." + str(symbol)).exists():
                        task.symbol = group_task.symbol + "." + str(symbol)
                        break
                task.group_task = group_task
                task.save()
                data['form_is_valid'] = True
                tasks = Task.objects.filter(group_task=group_task_code).order_by('create_time')
                context = {'group_task': group_task, 'project': project, 'task': task, 'form': form, 'tasks': tasks, 'request_user_is_business_analyst': request_user_is_business_analyst}
                context.update(csrf(request))
                data['html_task'] = render_to_string('project/task_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        task_form = TaskForm()
    context = {'project': project, 'group_task': group_task, 'task_form': task_form}
    data['html_task_form'] = render_to_string('project/task_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def task_edit(request, project_code, group_task_code, task_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    form = CommentForm(request.POST)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            data['form_is_valid'] = True
            tasks = Task.objects.filter(group_task=group_task_code)
            task.comments.clear()
            context = {'project': project, 'group_task': group_task, 'task': task, 'tasks': tasks, 'form': form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_task'] = render_to_string('project/task_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        task_form = TaskForm(instance=task)
    context = {'project': project, 'group_task': group_task, 'task': task, 'task_form': task_form}
    data['html_task_form'] = render_to_string('project/task_edit.html', context, request=request)
    return JsonResponse(data)


def task_detail(request, project_code, group_task_code, task_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    functions = Function.objects.filter(task=task_code).order_by('create_time')
    form = CommentForm(request.POST)
    member = project.member_set.get(user=request.user)
    context = {
        'project': project,
        'group_task': group_task,
        'task': task,
        'functions': functions,
        'form': form,
        'request_user_is_business_analyst': request_user_is_business_analyst,
        'role': member.get_role_display(),
    }
    return render(request, 'project/task_detail.html', context)


def task_comment_add(request, project_code, group_task_code, task_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            task.comments.add(comment)
            data['form_is_valid'] = True
            data['html_task_comment'] = render_to_string('project/task_comment_list.html', {'task': task})
            data['html_task_comment_number'] = render_to_string('project/task_comment_number.html', {'task': task})
        else:
            data['form_is_valid'] = False
    else:
        form = CommentForm()
    context = {'project': project, 'group_task': group_task, 'task': task, 'form': form}
    data['html_task_comment_form'] = render_to_string('project/task_comment_form.html', context, request=request)
    return JsonResponse(data)


def task_reversions(request, project_code, group_task_code, task_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    member = project.member_set.get(user=request.user)
    versions = Version.objects.get_for_object(task)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'group_task': group_task, 'task': task, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/task_reversions.html', context)


@reversion.create_revision()
def task_revert(request, project_code, group_task_code, task_code, task_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    revision = get_object_or_404(Version.objects.get_for_object(task), pk=task_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    task.comments.clear()
    return redirect('project:group_task_detail', project_code=project.code, group_task_code=group_task.code)


@reversion.create_revision()
def function_add(request, project_code, group_task_code, task_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    form = CommentForm(request.POST)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        function_form = FunctionForm(request.POST)
        if function_form.is_valid():
            name = function_form.cleaned_data['name']
            if Function.objects.filter(task=task_code, name=name).exists():
                function_form.add_error('name', _('Function with the same name is already exist in this task!'))
            else:
                function = function_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not Function.objects.filter(task=task_code, symbol=task.symbol + "." + str(symbol)).exists():
                        function.symbol = task.symbol + "." + str(symbol)
                        break
                function.task = task
                function.save()
                data['form_is_valid'] = True
                functions = Function.objects.filter(task=task_code).order_by('create_time')
                context = {'project': project, 'group_task': group_task, 'task': task, 'function': function, 'functions': functions, 'form': form, 'request_user_is_business_analyst': request_user_is_business_analyst}
                context.update(csrf(request))
                data['html_function'] = render_to_string('project/function_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        function_form = FunctionForm()
    context = {'project': project, 'group_task': group_task, 'task': task, 'function_form': function_form}
    data['html_function_form'] = render_to_string('project/function_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def function_edit(request, project_code, group_task_code, task_code, function_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    function = get_object_or_404(Function, pk=function_code)
    form = CommentForm(request.POST)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        function_form = FunctionForm(request.POST, instance=function)
        if function_form.is_valid():
            function_form.save()
            data['form_is_valid'] = True
            functions = Function.objects.filter(task=task_code)
            function.comments.clear()
            context = {'project': project, 'group_task': group_task, 'task': task, 'function': function, 'functions': functions, 'form': form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_function'] = render_to_string('project/function_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        function_form = FunctionForm(instance=function)
    context = {'project': project, 'group_task': group_task, 'task': task, 'function': function, 'function_form': function_form}
    data['html_function_form'] = render_to_string('project/function_edit.html', context, request=request)
    return JsonResponse(data)


def function_comment_add(request, project_code, group_task_code, task_code, function_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    function = get_object_or_404(Function, pk=function_code)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            function.comments.add(comment)
            data['form_is_valid'] = True
            data['html_function_comment'] = render_to_string('project/function_comment_list.html', {'function': function})
            data['html_function_comment_number'] = render_to_string('project/function_comment_number.html', {'function': function})
        else:
            data['form_is_valid'] = False
    else:
        form = CommentForm()
    context = {'project': project, 'group_task': group_task, 'task': task, 'function': function, 'form': form}
    data['html_function_comment_form'] = render_to_string('project/function_comment_form.html', context, request=request)
    return JsonResponse(data)


def function_reversions(request, project_code, group_task_code, task_code, function_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    function = get_object_or_404(Function, pk=function_code)
    member = project.member_set.get(user=request.user)
    versions = Version.objects.get_for_object(function)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'group_task': group_task, 'task': task, 'function': function, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/function_reversions.html', context)


@reversion.create_revision()
def function_revert(request, project_code, group_task_code, task_code, function_code, function_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_task = get_object_or_404(GroupTask, pk=group_task_code)
    task = get_object_or_404(Task, pk=task_code)
    function = get_object_or_404(Function, pk=function_code)
    revision = get_object_or_404(Version.objects.get_for_object(function), pk=function_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    function.comments.clear()
    return redirect('project:task_detail', project_code=project.code, group_task_code=group_task.code, task_code=task.code)


@reversion.create_revision()
def user_characteristic_add(request, project_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    user_characteristic_comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        user_characteristic_form = UserCharacteristicForm(request.POST)
        if user_characteristic_form.is_valid():
            user_class = user_characteristic_form.cleaned_data['user_class']
            user_symbol = user_characteristic_form.cleaned_data['user_symbol']
            if UserCharacteristic.objects.filter(user_class=user_class, project=project_code).exists():
                user_characteristic_form.add_error('user_class', _('The same user class is already exist!'))
            elif UserCharacteristic.objects.filter(user_symbol=user_symbol, project=project_code).exists():
                user_characteristic_form.add_error('user_symbol', _('The same user symbol is already exist!'))
            else:
                user_characteristic = user_characteristic_form.save(commit=False)
                user_characteristic.project = project
                user_characteristic.save()
                data['form_is_valid'] = True
                user_characteristics = UserCharacteristic.objects.filter(project=project_code).order_by('-create_time')
                context = {'project': project, 'user_characteristic': user_characteristic, 'user_characteristics': user_characteristics, 'request_user_is_business_analyst': request_user_is_business_analyst, 'user_characteristic_comment_form': user_characteristic_comment_form}
                context.update(csrf(request))
                data['html_user_characteristic'] = render_to_string('project/user_characteristic_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        user_characteristic_form = UserCharacteristicForm()
    context = {'project': project, 'user_characteristic_form': user_characteristic_form}
    data['html_user_characteristic_form'] = render_to_string('project/user_characteristic_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def user_characteristic_edit(request, project_code, user_characteristic_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    user_characteristic = get_object_or_404(UserCharacteristic, pk=user_characteristic_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    user_characteristic_comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        user_characteristic_form = UserCharacteristicForm(request.POST, instance=user_characteristic)
        if user_characteristic_form.is_valid():
            user_characteristic_form.save()
            data['form_is_valid'] = True
            user_characteristics = UserCharacteristic.objects.filter(project=project_code)
            user_characteristic.comments.clear()
            context = {'project': project, 'user_characteristic': user_characteristic, 'user_characteristics': user_characteristics, 'request_user_is_business_analyst': request_user_is_business_analyst, 'user_characteristic_comment_form': user_characteristic_comment_form}
            context.update(csrf(request))
            data['html_user_characteristic'] = render_to_string('project/user_characteristic_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        user_characteristic_form = UserCharacteristicForm(instance=user_characteristic)
    context = {'project': project, 'user_characteristic': user_characteristic, 'user_characteristic_form': user_characteristic_form}
    data['html_user_characteristic_form'] = render_to_string('project/user_characteristic_edit.html', context, request=request)
    return JsonResponse(data)


def user_characteristic_reversions(request, project_code, user_characteristic_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    user_characteristic = get_object_or_404(UserCharacteristic, pk=user_characteristic_code)
    member = project.member_set.get(user=request.user)
    versions = Version.objects.get_for_object(user_characteristic)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'user_characteristic': user_characteristic, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/user_characteristic_reversions.html', context)


@reversion.create_revision()
def user_characteristic_revert(request, project_code, user_characteristic_code, user_characteristic_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    user_characteristic = get_object_or_404(UserCharacteristic, pk=user_characteristic_code)
    revision = get_object_or_404(Version.objects.get_for_object(user_characteristic), pk=user_characteristic_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    user_characteristic.comments.clear()
    return redirect('project:project_detail', project_code=project.code)


def user_characteristic_comment_add(request, project_code, user_characteristic_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    user_characteristic = get_object_or_404(UserCharacteristic, pk=user_characteristic_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        user_characteristic_comment_form = CommentForm(request.POST)
        if user_characteristic_comment_form.is_valid():
            comment = user_characteristic_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            user_characteristic.comments.add(comment)
            data['form_is_valid'] = True
            context = {'user_characteristic': user_characteristic, 'request_user_is_business_analyst': request_user_is_business_analyst}
            data['html_user_characteristic_comment'] = render_to_string('project/user_characteristic_comment_list.html', context)
            data['html_user_characteristic_comment_number'] = render_to_string('project/user_characteristic_comment_number.html', {'user_characteristic': user_characteristic})
        else:
            data['form_is_valid'] = False
    else:
        user_characteristic_comment_form = CommentForm()
    context = {'project': project, 'user_characteristic': user_characteristic, 'user_characteristic_comment_form': user_characteristic_comment_form}
    data['html_user_characteristic_comment_form'] = render_to_string('project/user_characteristic_comment_form.html', context, request=request)
    return JsonResponse(data)


def user_characteristic_autocomplete(request):
    if request.is_ajax():
        word = request.GET.get('term', '')
        user_characteristics = UserCharacteristicDictionary.objects.filter(user_class__icontains=word)
        results = []
        for user_characteristic in user_characteristics:
            user_characteristic_json = {
                'id': user_characteristic.id,
                'label': user_characteristic.user_class,
                'value': user_characteristic.user_class,
                'user_symbol': user_characteristic.user_symbol,
                'user_description': user_characteristic.user_description
            }
            results.append(user_characteristic_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@reversion.create_revision()
def purpose_add(request, project_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    purpose_comment_form = CommentForm()
    if request.method == 'POST':
        purpose_form = PurposeForm(request.POST)
        if purpose_form.is_valid():
            purpose = purpose_form.save(commit=False)
            purpose.project = project
            purpose.save()
            data['form_is_valid'] = True
            purposes = Purpose.objects.filter(project=project_code)
            context = {'project': project, 'purpose': purpose, 'purposes': purposes, 'purpose_comment_form': purpose_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_purpose'] = render_to_string('project/purpose_list.html', context)
            data['html_purpose_top'] = render_to_string('project/purpose_top.html', {'project': project})
            reversion.set_user(request.user)
            reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        purpose_form = PurposeForm()
    context = {'project': project, 'purpose_form': purpose_form}
    data['html_purpose_form'] = render_to_string('project/purpose_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def purpose_edit(request, project_code, purpose_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    purpose = get_object_or_404(Purpose, pk=purpose_code)
    purpose_comment_form = CommentForm()
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        purpose_form = PurposeForm(request.POST, instance=purpose)
        if purpose_form.is_valid():
            purpose_form.save()
            data['form_is_valid'] = True
            purposes = Purpose.objects.filter(project=project_code)
            purpose.comments.clear()
            context = {'project': project, 'purpose': purpose, 'purposes': purposes, 'purpose_comment_form': purpose_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_purpose'] = render_to_string('project/purpose_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        purpose_form = PurposeForm(instance=purpose)
    context = {'project': project, 'purpose': purpose, 'purpose_form': purpose_form}
    data['html_purpose_form'] = render_to_string('project/purpose_edit.html', context, request=request)
    return JsonResponse(data)


def purpose_comment_add(request, project_code, purpose_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    purpose = get_object_or_404(Purpose, pk=purpose_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        purpose_comment_form = CommentForm(request.POST)
        if purpose_comment_form.is_valid():
            comment = purpose_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            purpose.comments.add(comment)
            data['form_is_valid'] = True
            context = {'purpose': purpose, 'request_user_is_business_analyst': request_user_is_business_analyst}
            data['html_purpose_comment'] = render_to_string('project/purpose_comment_list.html', context)
            data['html_purpose_comment_number'] = render_to_string('project/purpose_comment_number.html', {'purpose': purpose})
        else:
            data['form_is_valid'] = False
    else:
        purpose_comment_form = CommentForm()
    context = {'project': project, 'purpose': purpose, 'purpose_comment_form': purpose_comment_form}
    data['html_purpose_comment_form'] = render_to_string('project/purpose_comment_form.html', context, request=request)
    return JsonResponse(data)


def purpose_reversions(request, project_code, purpose_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    purpose = get_object_or_404(Purpose, pk=purpose_code)
    versions = Version.objects.get_for_object(purpose)
    member = project.member_set.get(user=request.user)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'purpose': purpose, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/purpose_reversions.html', context)


@reversion.create_revision()
def purpose_revert(request, project_code, purpose_code, purpose_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    purpose = get_object_or_404(Purpose, pk=purpose_code)
    revision = get_object_or_404(Version.objects.get_for_object(purpose), pk=purpose_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    purpose.comments.clear()
    return redirect('project:project_detail', project_code=project.code)


@reversion.create_revision()
def creation_goal_add(request, project_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    creation_goal_comment_form = CommentForm()
    if request.method == 'POST':
        creation_goal_form = CreationGoalForm(request.POST)
        if creation_goal_form.is_valid():
            creation_goal = creation_goal_form.save(commit=False)
            creation_goal.project = project
            creation_goal.save()
            data['form_is_valid'] = True
            creation_goals = CreationGoal.objects.filter(project=project_code)
            context = {'project': project, 'creation_goal': creation_goal, 'creation_goals': creation_goals, 'creation_goal_comment_form': creation_goal_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_creation_goal'] = render_to_string('project/creation_goal_list.html', context)
            data['html_creation_goal_top'] = render_to_string('project/creation_goal_top.html', {'project': project})
            reversion.set_user(request.user)
            reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        creation_goal_form = CreationGoalForm()
    context = {'project': project, 'creation_goal_form': creation_goal_form}
    data['html_creation_goal_form'] = render_to_string('project/creation_goal_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def creation_goal_edit(request, project_code, creation_goal_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    creation_goal = get_object_or_404(CreationGoal, pk=creation_goal_code)
    creation_goal_comment_form = CommentForm()
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        creation_goal_form = CreationGoalForm(request.POST, instance=creation_goal)
        if creation_goal_form.is_valid():
            creation_goal_form.save()
            data['form_is_valid'] = True
            creation_goals = CreationGoal.objects.filter(project=project_code)
            creation_goal.comments.clear()
            context = {'project': project, 'creation_goal': creation_goal, 'creation_goals': creation_goals, 'creation_goal_comment_form': creation_goal_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_creation_goal'] = render_to_string('project/creation_goal_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        creation_goal_form = CreationGoalForm(instance=creation_goal)
    context = {'project': project, 'creation_goal': creation_goal, 'creation_goal_form': creation_goal_form}
    data['html_creation_goal_form'] = render_to_string('project/creation_goal_edit.html', context, request=request)
    return JsonResponse(data)


def creation_goal_comment_add(request, project_code, creation_goal_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    creation_goal = get_object_or_404(CreationGoal, pk=creation_goal_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        creation_goal_comment_form = CommentForm(request.POST)
        if creation_goal_comment_form.is_valid():
            comment = creation_goal_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            creation_goal.comments.add(comment)
            data['form_is_valid'] = True
            context = {'creation_goal': creation_goal, 'request_user_is_business_analyst': request_user_is_business_analyst}
            data['html_creation_goal_comment'] = render_to_string('project/creation_goal_comment_list.html', context)
            data['html_creation_goal_comment_number'] = render_to_string('project/creation_goal_comment_number.html', {'creation_goal': creation_goal})
        else:
            data['form_is_valid'] = False
    else:
        creation_goal_comment_form = CommentForm()
    context = {'project': project, 'creation_goal': creation_goal, 'creation_goal_comment_form': creation_goal_comment_form}
    data['html_creation_goal_comment_form'] = render_to_string('project/creation_goal_comment_form.html', context, request=request)
    return JsonResponse(data)


def creation_goal_reversions(request, project_code, creation_goal_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    creation_goal = get_object_or_404(CreationGoal, pk=creation_goal_code)
    versions = Version.objects.get_for_object(creation_goal)
    member = project.member_set.get(user=request.user)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'creation_goal': creation_goal, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/creation_goal_reversions.html', context)


@reversion.create_revision()
def creation_goal_revert(request, project_code, creation_goal_code, creation_goal_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    creation_goal = get_object_or_404(CreationGoal, pk=creation_goal_code)
    revision = get_object_or_404(Version.objects.get_for_object(creation_goal), pk=creation_goal_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    creation_goal.comments.clear()
    return redirect('project:project_detail', project_code=project.code)


@reversion.create_revision()
def object_information_add(request, project_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    object_information_comment_form = CommentForm()
    if request.method == 'POST':
        object_information_form = ObjectInformationForm(request.POST)
        if object_information_form.is_valid():
            object_information = object_information_form.save(commit=False)
            object_information.project = project
            object_information.save()
            data['form_is_valid'] = True
            object_information_all = ObjectInformation.objects.filter(project=project_code)
            context = {'project': project, 'object_information': object_information, 'object_information_all': object_information_all, 'object_information_comment_form': object_information_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_object_information'] = render_to_string('project/object_information_list.html', context)
            data['html_object_information_top'] = render_to_string('project/object_information_top.html', {'project': project})
            reversion.set_user(request.user)
            reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        object_information_form = ObjectInformationForm()
    context = {'project': project, 'object_information_form': object_information_form}
    data['html_object_information_form'] = render_to_string('project/object_information_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def object_information_edit(request, project_code, object_information_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    object_information = get_object_or_404(ObjectInformation, pk=object_information_code)
    object_information_comment_form = CommentForm()
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        object_information_form = ObjectInformationForm(request.POST, instance=object_information)
        if object_information_form.is_valid():
            object_information_form.save()
            data['form_is_valid'] = True
            object_information_all = ObjectInformation.objects.filter(project=project_code)
            object_information.comments.clear()
            context = {'project': project, 'object_information': object_information, 'object_information_all': object_information_all, 'object_information_comment_form': object_information_comment_form, 'request_user_is_business_analyst': request_user_is_business_analyst}
            context.update(csrf(request))
            data['html_object_information'] = render_to_string('project/object_information_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        object_information_form = ObjectInformationForm(instance=object_information)
    context = {'project': project, 'object_information': object_information, 'object_information_form': object_information_form}
    data['html_object_information_form'] = render_to_string('project/object_information_edit.html', context, request=request)
    return JsonResponse(data)


def object_information_comment_add(request, project_code, object_information_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    object_information = get_object_or_404(ObjectInformation, pk=object_information_code)
    request_user_is_business_analyst = project.member_set.filter(user=request.user, role='business_analyst').exists()
    if request.method == 'POST':
        object_information_comment_form = CommentForm(request.POST)
        if object_information_comment_form.is_valid():
            comment = object_information_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            object_information.comments.add(comment)
            data['form_is_valid'] = True
            context = {'object_information': object_information, 'request_user_is_business_analyst': request_user_is_business_analyst}
            data['html_object_information_comment'] = render_to_string('project/object_information_comment_list.html', context)
            data['html_object_information_comment_number'] = render_to_string('project/object_information_comment_number.html', {'object_information': object_information})
        else:
            data['form_is_valid'] = False
    else:
        object_information_comment_form = CommentForm()
    context = {'project': project, 'object_information': object_information, 'object_information_comment_form': object_information_comment_form}
    data['html_object_information_comment_form'] = render_to_string('project/object_information_comment_form.html', context, request=request)
    return JsonResponse(data)


def object_information_reversions(request, project_code, object_information_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    object_information = get_object_or_404(ObjectInformation, pk=object_information_code)
    versions = Version.objects.get_for_object(object_information)
    member = project.member_set.get(user=request.user)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'object_information': object_information, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/object_information_reversions.html', context)


@reversion.create_revision()
def object_information_revert(request, project_code, object_information_code, object_information_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    object_information = get_object_or_404(ObjectInformation, pk=object_information_code)
    revision = get_object_or_404(Version.objects.get_for_object(object_information), pk=object_information_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    object_information.comments.clear()
    return redirect('project:project_detail', project_code=project.code)


def group_requirement_type_add(request, project_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    group_requirement_types = GroupRequirementType.objects.filter(project=project_code, is_visible=True)

    # START: CREATE TYPES FROM DICTIONARY
    objects = GroupRequirementType.objects.filter(project=project_code)
    current_list = []
    for x in objects:
        v = (x.symbol, x.name)
        current_list.append(v)
    full_list = [(x.symbol, x.name) for x in GroupRequirementTypeDictionary.objects.all()]
    for item in full_list:
        if item not in current_list:
            group_requirement_type = GroupRequirementType.objects.create(project=project, symbol=item[0], name=item[1])
            group_requirement_type.save()
    # END: CREATE TYPES FROM DICTIONARY

    group_requirement_type_formset = GroupRequirementTypeFormSet(request.POST or None, queryset=GroupRequirementType.objects.all())
    if request.method == 'POST':
        if group_requirement_type_formset.is_valid():
            group_requirement_type_formset.save()
            data['form_is_valid'] = True
            context = {'project': project, 'group_requirement_types': group_requirement_types, 'group_requirement_type_formset': group_requirement_type_formset, 'request_user_is_system_analyst': request_user_is_system_analyst}
            context.update(csrf(request))
            data['html_group_requirement_type'] = render_to_string('project/group_requirement_type_list.html', context)
        else:
            data['form_is_valid'] = False
    else:
        group_requirement_type_formset = GroupRequirementTypeFormSet()
    data['html_group_requirement_type_form'] = render_to_string('project/group_requirement_type_add.html', {'project': project, 'group_requirement_type_formset': group_requirement_type_formset}, request=request)
    return JsonResponse(data)


def group_requirement_type_detail(request, project_code, group_requirement_type_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    member = project.member_set.get(user=request.user)
    group_requirement_comment_form = CommentForm(request.POST)
    group_requirements = GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code).order_by('create_time')
    context = {
        'project': project,
        'group_requirement_type': group_requirement_type,
        'request_user_is_system_analyst': request_user_is_system_analyst,
        'role': member.get_role_display(),
        'group_requirement_comment_form': group_requirement_comment_form,
        'group_requirements': group_requirements
    }
    return render(request, 'project/group_requirement_type_detail.html', context)


@reversion.create_revision()
def group_requirement_add(request, project_code, group_requirement_type_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    group_requirement_comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        group_requirement_form = GroupRequirementForm(request.POST)
        if group_requirement_form.is_valid():
            name = group_requirement_form.cleaned_data['name']
            if GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code, name=name).exists():
                group_requirement_form.add_error('name', _('Group requirement with the same name is already exist in this type!'))
            else:
                group_requirement = group_requirement_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code, symbol=group_requirement_type.symbol + "." + "{0:0=2d}".format(symbol) + "." + "00").exists():
                        group_requirement.symbol = group_requirement_type.symbol + "." + "{0:0=2d}".format(symbol) + "." + "00"
                        break
                group_requirement.group_requirement_type = group_requirement_type
                group_requirement.save()
                data['form_is_valid'] = True
                group_requirements = GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code).order_by('create_time')
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirements': group_requirements, 'group_requirement_comment_form': group_requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_group_requirement'] = render_to_string('project/group_requirement_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        group_requirement_form = GroupRequirementForm()
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement_form': group_requirement_form}
    data['html_group_requirement_form'] = render_to_string('project/group_requirement_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def group_requirement_edit(request, project_code, group_requirement_type_code, group_requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    group_requirement_comment_form = CommentForm(request.POST)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    if request.method == 'POST':
        group_requirement_form = GroupRequirementForm(request.POST, instance=group_requirement)
        if group_requirement_form.is_valid():
            group_requirement_form.save()
            data['form_is_valid'] = True
            group_requirements = GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code)
            group_requirement.comments.clear()
            context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'group_requirements': group_requirements, 'group_requirement_comment_form': group_requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
            context.update(csrf(request))
            data['html_group_requirement'] = render_to_string('project/group_requirement_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        group_requirement_form = GroupRequirementForm(instance=group_requirement)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'group_requirement_form': group_requirement_form}
    data['html_group_requirement_form'] = render_to_string('project/group_requirement_edit.html', context, request=request)
    return JsonResponse(data)


def group_requirement_detail(request, project_code, group_requirement_type_code, group_requirement_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirements = Requirement.objects.filter(group_requirement=group_requirement_code).order_by('create_time')
    requirement_comment_form = CommentForm(request.POST)
    member = project.member_set.get(user=request.user)
    context = {
        'project': project,
        'group_requirement_type': group_requirement_type,
        'group_requirement': group_requirement,
        'requirements': requirements,
        'requirement_comment_form': requirement_comment_form,
        'request_user_is_system_analyst': request_user_is_system_analyst,
        'role': member.get_role_display(),
    }
    return render(request, 'project/group_requirement_detail.html', context)


def group_requirement_comment_add(request, project_code, group_requirement_type_code, group_requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    if request.method == 'POST':
        group_requirement_comment_form = CommentForm(request.POST)
        if group_requirement_comment_form.is_valid():
            comment = group_requirement_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            group_requirement.comments.add(comment)
            data['form_is_valid'] = True
            context = {'group_requirement': group_requirement, 'request_user_is_system_analyst': request_user_is_system_analyst}
            data['html_group_requirement_comment'] = render_to_string('project/group_requirement_comment_list.html', context)
            data['html_group_requirement_comment_number'] = render_to_string('project/group_requirement_comment_number.html', {'group_requirement': group_requirement})
        else:
            data['form_is_valid'] = False
    else:
        group_requirement_comment_form = CommentForm()
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'group_requirement_comment_form': group_requirement_comment_form}
    data['html_group_requirement_comment_form'] = render_to_string('project/group_requirement_comment_form.html', context, request=request)
    return JsonResponse(data)


def group_requirement_reversions(request, project_code, group_requirement_type_code, group_requirement_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    versions = Version.objects.get_for_object(group_requirement)
    member = project.member_set.get(user=request.user)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/group_requirement_reversions.html', context)


@reversion.create_revision()
def group_requirement_revert(request, project_code, group_requirement_type_code, group_requirement_code, group_requirement_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    revision = get_object_or_404(Version.objects.get_for_object(group_requirement), pk=group_requirement_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    group_requirement.comments.clear()
    return redirect('project:group_requirement_type_detail', project_code=project.code, group_requirement_type_code=group_requirement_type.code)


@reversion.create_revision()
def requirement_add(request, project_code, group_requirement_type_code, group_requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirement_comment_form = CommentForm(request.POST)
    group_tasks = GroupTask.objects.filter(project=project_code)
    group_task_codes = [str(group_task.code) for group_task in group_tasks]
    tasks = Task.objects.filter(group_task__in=group_task_codes)
    task_codes = [str(task.code) for task in tasks]
    all_functions = Function.objects.filter(task__in=task_codes).order_by('symbol', 'create_time')
    if request.method == 'POST':
        requirement_form = RequirementForm(data=request.POST, all_functions=all_functions)
        # requirement_form = RequirementFormTree(data=request.POST or None, all_functions=all_functions)
        if requirement_form.is_valid():
            description = requirement_form.cleaned_data['description']
            if Requirement.objects.filter(group_requirement=group_requirement_code, description=description).exists():
                requirement_form.add_error('description', _('Requirement with the same description is already exist!'))
            else:
                requirement = requirement_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not Requirement.objects.filter(group_requirement=group_requirement_code, symbol=re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)).exists():
                        requirement.symbol = re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)
                        break
                requirement.group_requirement = group_requirement
                requirement.save()
                requirement_form.save_m2m()
                data['form_is_valid'] = True
                requirements = Requirement.objects.filter(group_requirement=group_requirement_code).order_by('create_time')
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_requirement'] = render_to_string('project/requirement_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        requirement_form = RequirementForm(all_functions=all_functions)
        # requirement_form = RequirementFormTree(all_functions=all_functions)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def requirement_edit(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    requirement_comment_form = CommentForm(request.POST)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    group_tasks = GroupTask.objects.filter(project=project_code)
    group_task_codes = [str(group_task.code) for group_task in group_tasks]
    tasks = Task.objects.filter(group_task__in=group_task_codes)
    task_codes = [str(task.code) for task in tasks]
    all_functions = Function.objects.filter(task__in=task_codes).order_by('symbol', 'create_time')
    if request.method == 'POST':
        # requirement_form = RequirementForm(request.POST, instance=requirement, all_functions=all_functions)
        requirement_form = RequirementFormTree(data=request.POST, instance=requirement, all_functions=all_functions)
        if requirement_form.is_valid():
            requirement_form.save()
            data['form_is_valid'] = True
            requirements = Requirement.objects.filter(group_requirement=group_requirement_code)
            requirement.comments.clear()
            context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
            context.update(csrf(request))
            data['html_requirement'] = render_to_string('project/requirement_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        # requirement_form = RequirementForm(instance=requirement, all_functions=all_functions)
        requirement_form = RequirementFormTree(instance=requirement, all_functions=all_functions)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_edit.html', context, request=request)
    return JsonResponse(data)


def requirement_detail(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    request_user_is_developer = project.member_set.filter(user=request.user, role='developer').exists()
    member = project.member_set.get(user=request.user)
    specification_comment_form = CommentForm(request.POST)
    specifications = Specification.objects.filter(requirement=requirement_code)
    specification_is_exist = Specification.objects.filter(requirement=requirement_code).exists()
    context = {
        'project': project,
        'group_requirement_type': group_requirement_type,
        'group_requirement': group_requirement,
        'requirement': requirement,
        'specifications': specifications,
        'specification_comment_form': specification_comment_form,
        'request_user_is_developer': request_user_is_developer,
        'specification_is_exist': specification_is_exist,
        'role': member.get_role_display(),
    }
    return render(request, 'project/requirement_detail.html', context)


def requirement_comment_add(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    if request.method == 'POST':
        requirement_comment_form = CommentForm(request.POST)
        if requirement_comment_form.is_valid():
            comment = requirement_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            requirement.comments.add(comment)
            data['form_is_valid'] = True
            context = {'requirement': requirement, 'request_user_is_system_analyst': request_user_is_system_analyst}
            data['html_requirement_comment'] = render_to_string('project/requirement_comment_list.html', context)
            data['html_requirement_comment_number'] = render_to_string('project/requirement_comment_number.html', {'requirement': requirement})
        else:
            data['form_is_valid'] = False
    else:
        requirement_comment_form = CommentForm()
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirement_comment_form': requirement_comment_form}
    data['html_requirement_comment_form'] = render_to_string('project/requirement_comment_form.html', context, request=request)
    return JsonResponse(data)


def requirement_reversions(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    versions = Version.objects.get_for_object(requirement)
    member = project.member_set.get(user=request.user)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
        version.function = Function.objects.filter(code__in=version.field_dict['function'])
        version.user_characteristic = UserCharacteristic.objects.filter(code__in=version.field_dict['user_characteristic'])
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/requirement_reversions.html', context)


@reversion.create_revision()
def requirement_revert(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code, requirement_reversion_id):
    project = get_object_or_404(Project, pk=project_code, status='open')
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    revision = get_object_or_404(Version.objects.get_for_object(requirement), pk=requirement_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    requirement.comments.clear()
    return redirect('project:group_requirement_detail', project_code=project.code, group_requirement_type_code=group_requirement_type.code, group_requirement_code=group_requirement.code)


@reversion.create_revision()
def v_requirement_add(request, project_code, group_requirement_type_code, group_requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirement_comment_form = CommentForm(request.POST)
    all_user_characteristics = UserCharacteristic.objects.filter(project=project_code)
    if request.method == 'POST':
        requirement_form = V_RequirementForm(data=request.POST, all_user_characteristics=all_user_characteristics)
        if requirement_form.is_valid():
            description = requirement_form.cleaned_data['description']
            if Requirement.objects.filter(group_requirement=group_requirement_code, description=description).exists():
                requirement_form.add_error('description', _('Requirement with the same description is already exist!'))
            else:
                requirement = requirement_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not Requirement.objects.filter(group_requirement=group_requirement_code, symbol=re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)).exists():
                        requirement.symbol = re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)
                        break
                requirement.group_requirement = group_requirement
                requirement.save()
                requirement_form.save_m2m()
                data['form_is_valid'] = True
                requirements = Requirement.objects.filter(group_requirement=group_requirement_code)
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_requirement'] = render_to_string('project/requirement_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        requirement_form = V_RequirementForm(all_user_characteristics=all_user_characteristics)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def v_requirement_edit(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirement_comment_form = CommentForm(request.POST)
    all_user_characteristics = UserCharacteristic.objects.filter(project=project_code)
    if request.method == 'POST':
        requirement_form = V_RequirementForm(data=request.POST, instance=requirement, all_user_characteristics=all_user_characteristics)
        if requirement_form.is_valid():
            requirement_form.save()
            data['form_is_valid'] = True
            requirements = Requirement.objects.filter(group_requirement=group_requirement_code)
            requirement.comments.clear()
            context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
            context.update(csrf(request))
            data['html_requirement'] = render_to_string('project/requirement_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        requirement_form = V_RequirementForm(instance=requirement, all_user_characteristics=all_user_characteristics)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_edit.html', context, request=request)
    return JsonResponse(data)


def fa_group_requirement_add(request, project_code, group_requirement_type_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()

    # START: Формирование списка задач
    group_tasks = GroupTask.objects.filter(project=project_code)
    group_task_codes = [str(group_task.code) for group_task in group_tasks]
    tasks = Task.objects.filter(group_task__in=group_task_codes)
    all_tasks = tasks
    # END: Формирование списка задач

    if request.method == 'POST':
        group_requirement_form = FA_GroupRequirementForm(data=request.POST, all_tasks=all_tasks)
        if group_requirement_form.is_valid():
            task = group_requirement_form.cleaned_data['task']
            if GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code, task=task).exists():
                group_requirement_form.add_error('task', _('Group requirement with the same task is already exist!'))
            else:
                group_requirement = group_requirement_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code, symbol=group_requirement_type.symbol + "." + "{0:0=2d}".format(symbol) + "." + "00").exists():
                        group_requirement.symbol = group_requirement_type.symbol + "." + "{0:0=2d}".format(symbol) + "." + "00"
                        break
                group_requirement.group_requirement_type = group_requirement_type
                group_requirement.description = str(task)
                group_requirement.save()
                data['form_is_valid'] = True
                group_requirements = GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code)
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirements': group_requirements, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_group_requirement'] = render_to_string('project/group_requirement_tbody.html', context)
        else:
            data['form_is_valid'] = False
    else:
        group_requirement_form = FA_GroupRequirementForm(all_tasks=all_tasks)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement_form': group_requirement_form}
    data['html_group_requirement_form'] = render_to_string('project/group_requirement_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def fa_requirement_add(request, project_code, group_requirement_type_code, group_requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirement_comment_form = CommentForm(request.POST)

    all_functions = Function.objects.filter(task=group_requirement.task.code)
    all_user_characteristics = UserCharacteristic.objects.filter(project=project_code)

    if request.method == 'POST':
        requirement_form = FA_RequirementForm(data=request.POST, all_functions=all_functions, all_user_characteristics=all_user_characteristics)
        if requirement_form.is_valid():
            function = requirement_form.cleaned_data['function']
            if Requirement.objects.filter(group_requirement=group_requirement_code, function=function).exists():
                requirement_form.add_error('function', _('Requirement with the same function is already exist!'))
            else:
                requirement = requirement_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not Requirement.objects.filter(group_requirement=group_requirement_code, symbol=re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)).exists():
                        requirement.symbol = re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)
                        break
                requirement.group_requirement = group_requirement
                requirement.description = str(function.first())
                requirement.save()
                requirement_form.save_m2m()
                data['form_is_valid'] = True
                requirements = Requirement.objects.filter(group_requirement=group_requirement_code)
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_requirement'] = render_to_string('project/requirement_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        requirement_form = FA_RequirementForm(all_functions=all_functions, all_user_characteristics=all_user_characteristics)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def fa_requirement_edit(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirement_comment_form = CommentForm(request.POST)
    all_functions = Function.objects.filter(task=group_requirement.task.code)
    all_user_characteristics = UserCharacteristic.objects.filter(project=project_code)
    if request.method == 'POST':
        requirement_form = FA_RequirementForm(data=request.POST, instance=requirement, all_functions=all_functions, all_user_characteristics=all_user_characteristics)
        if requirement_form.is_valid():
            function = requirement_form.cleaned_data['function']
            if Requirement.objects.filter(group_requirement=group_requirement_code, function=function).exists():
                requirement_form.add_error('function', _('Requirement with the same function is already exist!'))
            else:
                requirement_form.save()
                data['form_is_valid'] = True
                requirements = Requirement.objects.filter(group_requirement=group_requirement_code)
                requirement.comments.clear()
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_requirement'] = render_to_string('project/requirement_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        requirement_form = FA_RequirementForm(instance=requirement, all_functions=all_functions, all_user_characteristics=all_user_characteristics)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_edit.html', context, request=request)
    return JsonResponse(data)


def df_group_requirement_add(request, project_code, group_requirement_type_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()

    # START: Формирование списка задач
    group_tasks = GroupTask.objects.filter(project=project_code)
    group_task_codes = [str(group_task.code) for group_task in group_tasks]
    tasks = Task.objects.filter(group_task__in=group_task_codes)
    all_tasks = tasks
    # END: Формирование списка задач

    if request.method == 'POST':
        group_requirement_form = DF_GroupRequirementForm(data=request.POST, all_tasks=all_tasks)
        if group_requirement_form.is_valid():
            task = group_requirement_form.cleaned_data['task']
            if GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code, task=task).exists():
                group_requirement_form.add_error('task', _('Group requirement with the same task is already exist!'))
            else:
                group_requirement = group_requirement_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code, symbol=group_requirement_type.symbol + "." + "{0:0=2d}".format(symbol) + "." + "00").exists():
                        group_requirement.symbol = group_requirement_type.symbol + "." + "{0:0=2d}".format(symbol) + "." + "00"
                        break
                group_requirement.group_requirement_type = group_requirement_type
                group_requirement.save()
                data['form_is_valid'] = True
                group_requirements = GroupRequirement.objects.filter(group_requirement_type=group_requirement_type_code)
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirements': group_requirements, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_group_requirement'] = render_to_string('project/group_requirement_tbody.html', context)
        else:
            data['form_is_valid'] = False
    else:
        group_requirement_form = DF_GroupRequirementForm(all_tasks=all_tasks)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement_form': group_requirement_form}
    data['html_group_requirement_form'] = render_to_string('project/group_requirement_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def df_requirement_add(request, project_code, group_requirement_type_code, group_requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirement_comment_form = CommentForm(request.POST)

    group_tasks = GroupTask.objects.filter(project=project_code)
    group_task_codes = [str(group_task.code) for group_task in group_tasks]
    tasks = Task.objects.filter(group_task__in=group_task_codes)
    task_codes = [str(task.code) for task in tasks]
    all_functions = Function.objects.filter(task__in=task_codes).order_by('create_time')

    if request.method == 'POST':
        requirement_form = DF_RequirementForm(data=request.POST, all_functions=all_functions)
        if requirement_form.is_valid():
            function = requirement_form.cleaned_data['function']
            if Requirement.objects.filter(group_requirement=group_requirement_code, function=function).exists():
                requirement_form.add_error('function', _('Requirement with the same function is already exist!'))
            else:
                requirement = requirement_form.save(commit=False)
                symbol = 0
                while True:
                    symbol = symbol + 1
                    if not Requirement.objects.filter(group_requirement=group_requirement_code, symbol=re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)).exists():
                        requirement.symbol = re.sub("00", "{0:0=2d}".format(symbol), group_requirement.symbol)
                        break
                requirement.group_requirement = group_requirement
                requirement.save()
                requirement_form.save_m2m()
                data['form_is_valid'] = True
                requirements = Requirement.objects.filter(group_requirement=group_requirement_code)
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_requirement'] = render_to_string('project/requirement_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        requirement_form = DF_RequirementForm(all_functions=all_functions)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def df_requirement_edit(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    request_user_is_system_analyst = project.member_set.filter(user=request.user, role='system_analyst').exists()
    requirement_comment_form = CommentForm(request.POST)

    group_tasks = GroupTask.objects.filter(project=project_code)
    group_task_codes = [str(group_task.code) for group_task in group_tasks]
    tasks = Task.objects.filter(group_task__in=group_task_codes)
    task_codes = [str(task.code) for task in tasks]
    all_functions = Function.objects.filter(task__in=task_codes).order_by('create_time')

    if request.method == 'POST':
        requirement_form = DF_RequirementForm(data=request.POST, instance=requirement, all_functions=all_functions)
        if requirement_form.is_valid():
            function = requirement_form.cleaned_data['function']
            if Requirement.objects.filter(group_requirement=group_requirement_code, function=function).exists():
                requirement_form.add_error('function', _('Requirement with the same function is already exist!'))
            else:
                requirement_form.save()
                data['form_is_valid'] = True
                requirements = Requirement.objects.filter(group_requirement=group_requirement_code)
                requirement.comments.clear()
                context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirements': requirements, 'requirement_comment_form': requirement_comment_form, 'request_user_is_system_analyst': request_user_is_system_analyst}
                context.update(csrf(request))
                data['html_requirement'] = render_to_string('project/requirement_list.html', context)
                reversion.set_user(request.user)
                reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        requirement_form = DF_RequirementForm(instance=requirement, all_functions=all_functions)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'requirement_form': requirement_form}
    data['html_requirement_form'] = render_to_string('project/requirement_edit.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def specification_add(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    request_user_is_developer = project.member_set.filter(user=request.user, role='developer').exists()
    specification_comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        specification_form = SpecificationForm(request.POST, request.FILES)
        if specification_form.is_valid():
            specification = specification_form.save(commit=False)
            symbol = 0
            while True:
                symbol = symbol + 1
                if not Specification.objects.filter(requirement=requirement_code, symbol=requirement.symbol + "." + "{0:0=2d}".format(symbol)).exists():
                    print(requirement.symbol + "." + "{0:0=2d}".format(symbol))
                    specification.symbol = str(requirement.symbol) + "." + "{0:0=2d}".format(symbol)
                    break
            specification.requirement = requirement
            specification.save()
            data['form_is_valid'] = True
            specifications = Specification.objects.filter(requirement=requirement_code).order_by('create_time')
            context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'specifications': specifications, 'specification_comment_form': specification_comment_form, 'request_user_is_developer': request_user_is_developer}
            context.update(csrf(request))
            data['html_specification'] = render_to_string('project/specification_list.html', context)
            data['html_specification_top'] = render_to_string('project/specification_top.html', {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement})
            reversion.set_user(request.user)
            reversion.set_comment('CREATE')
        else:
            data['form_is_valid'] = False
    else:
        specification_form = SpecificationForm()
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'specification_form': specification_form}
    data['html_specification_form'] = render_to_string('project/specification_add.html', context, request=request)
    return JsonResponse(data)


@reversion.create_revision()
def specification_edit(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code, specification_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    specification = get_object_or_404(Specification, pk=specification_code)
    specification_comment_form = CommentForm(request.POST)
    request_user_is_developer = project.member_set.filter(user=request.user, role='developer').exists()
    if request.method == 'POST':
        specification_form = SpecificationForm(request.POST, request.FILES, instance=specification)
        if specification_form.is_valid():
            specification_form.save()
            data['form_is_valid'] = True
            specifications = Specification.objects.filter(requirement=requirement_code)
            specification.comments.clear()
            context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'specifications': specifications, 'specification_comment_form': specification_comment_form, 'request_user_is_developer': request_user_is_developer}
            context.update(csrf(request))
            data['html_specification'] = render_to_string('project/specification_list.html', context)
            reversion.set_user(request.user)
            reversion.set_comment('EDIT')
        else:
            data['form_is_valid'] = False
    else:
        specification_form = SpecificationForm(instance=specification)
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'specification': specification, 'specification_form': specification_form}
    data['html_specification_form'] = render_to_string('project/specification_edit.html', context, request=request)
    return JsonResponse(data)


def specification_comment_add(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code, specification_code):
    data = dict()
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    specification = get_object_or_404(Specification, pk=specification_code)
    request_user_is_developer = project.member_set.filter(user=request.user, role='developer').exists()
    if request.method == 'POST':
        specification_comment_form = CommentForm(request.POST)
        if specification_comment_form.is_valid():
            comment = specification_comment_form.save(commit=False)
            comment.author = request.user
            comment.save()
            specification.comments.add(comment)
            data['form_is_valid'] = True
            context = {'specification': specification, 'request_user_is_developer': request_user_is_developer}
            data['html_specification_comment'] = render_to_string('project/specification_comment_list.html', context)
            data['html_specification_comment_number'] = render_to_string('project/specification_comment_number.html', {'specification': specification})
        else:
            data['form_is_valid'] = False
    else:
        specification_comment_form = CommentForm()
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'specification': specification, 'specification_comment_form': specification_comment_form}
    data['html_specification_comment_form'] = render_to_string('project/specification_comment_form.html', context, request=request)
    return JsonResponse(data)


def specification_reversions(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code, specification_code):
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    specification = get_object_or_404(Specification, pk=specification_code)
    versions = Version.objects.get_for_object(specification)
    member = project.member_set.get(user=request.user)
    for version in versions:
        version.comments = Comment.objects.filter(id__in=version.field_dict['comments'])
    context = {'project': project, 'group_requirement_type': group_requirement_type, 'group_requirement': group_requirement, 'requirement': requirement, 'specification': specification, 'versions': versions, 'role': member.get_role_display()}
    return render(request, 'project/specification_reversions.html', context)


@reversion.create_revision()
def specification_revert(request, project_code, group_requirement_type_code, group_requirement_code, requirement_code, specification_code, specification_reversion_id):
    project = get_object_or_404(Project, pk=project_code)
    group_requirement_type = get_object_or_404(GroupRequirementType, pk=group_requirement_type_code)
    group_requirement = get_object_or_404(GroupRequirement, pk=group_requirement_code)
    requirement = get_object_or_404(Requirement, pk=requirement_code)
    specification = get_object_or_404(Specification, pk=specification_code)
    revision = get_object_or_404(Version.objects.get_for_object(specification), pk=specification_reversion_id).revision
    revision_id = revision.id
    reversion.set_user(request.user)
    reversion.set_comment("REVERT to version: {}".format(revision_id))
    revision.revert()
    specification.comments.clear()
    return redirect('project:requirement_detail', project_code=project.code, group_requirement_type_code=group_requirement_type.code, group_requirement_code=group_requirement.code, requirement_code=requirement.code)


def generate_pdf(request, project_code):
    """
        Generate pdf file | Создание pdf файла
    """
    # Данные модели
    project = get_object_or_404(Project, pk=project_code, status='open')
    purposes = Purpose.objects.filter(project=project_code)
    creation_goals = CreationGoal.objects.filter(project=project_code)
    object_information_all = ObjectInformation.objects.filter(project=project_code)
    user_characteristics = UserCharacteristic.objects.filter(project=project_code).order_by('-create_time')
    group_tasks = GroupTask.objects.filter(project=project_code).order_by('create_time', 'symbol')
    group_requirement_types = GroupRequirementType.objects.filter(project=project_code, is_visible=True)
    html_template = get_template('project/pdf.html')
    rendered_html = html_template.render(RequestContext(request, {'project': project, 'user_characteristics': user_characteristics, 'purposes': purposes, 'creation_goals': creation_goals, 'object_information_all': object_information_all, 'group_tasks': group_tasks, 'group_requirement_types': group_requirement_types}))
    pdf_file = HTML(string=rendered_html).write_pdf()
    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="document.pdf"'
    return http_response
