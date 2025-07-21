from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Task, Project, Team
from .forms import TaskForm, ProjectForm, TeamForm, UserCreationForm
from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from django.shortcuts import render



# In-memory events (you can switch to DB later)
EVENTS = []

# ========== Dashboard ==========
@login_required
def dashboard_view(request):
    user_tasks = Task.objects.filter(assigned_to=request.user, status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS]).order_by('due_date')[:5]
    recent_projects = Project.objects.filter(created_by=request.user).order_by('-created_at')[:3]
    return render(request, 'dashboard.html', {
        'username': request.user.username,
        'page_title': 'Dashboard',
        'user_tasks': user_tasks,
        'recent_projects': recent_projects,
    })

# ========== Signup ==========
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'page_title': 'Sign Up',
        'form_title': 'Create Your Account',
    })

# ========== Tasks ==========
@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by('status', 'due_date')
    return render(request, 'planner/task_list.html', {
        'tasks': tasks,
        'page_title': 'All Tasks',
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'planner/task_form.html', {
        'form': form,
        'page_title': 'Create New Task',
        'form_title': 'Create Task',
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.created_by and request.user not in task.assigned_to.all():
        messages.error(request, "You don't have permission to edit this task.")
        return redirect('task_list')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'planner/task_form.html', {
        'form': form,
        'page_title': f'Edit Task: {task.name}',
        'form_title': 'Edit Task',
        'task': task,
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.created_by:
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'planner/task_confirm_delete.html', {
        'object': task,
        'page_title': 'Delete Task',
    })

# ========== Projects ==========
@login_required
def project_list(request):
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'planner/project_list.html', {
        'projects': projects,
        'page_title': 'All Projects',
    })

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'planner/project_form.html', {
        'form': form,
        'page_title': 'Create New Project',
        'form_title': 'Create Project',
    })

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.created_by:
        messages.error(request, "You don't have permission to edit this project.")
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'planner/project_form.html', {
        'form': form,
        'page_title': f'Edit Project: {project.name}',
        'form_title': 'Edit Project',
        'project': project,
    })

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.created_by:
        messages.error(request, "You don't have permission to delete this project.")
        return redirect('project_list')

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('project_list')
    return render(request, 'planner/project_confirm_delete.html', {
        'object': project,
        'page_title': 'Delete Project',
    })

# ========== Teams ==========
@login_required
def team_list(request):
    teams = Team.objects.filter(members=request.user).distinct().order_by('name')
    return render(request, 'planner/team_list.html', {
        'teams': teams,
        'page_title': 'All Teams',
    })

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            team.members.add(request.user)
            messages.success(request, 'Team created successfully!')
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'planner/team_form.html', {
        'form': form,
        'page_title': 'Create New Team',
        'form_title': 'Create Team',
    })

@login_required
def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.user not in team.members.all():
        messages.error(request, "You don't have permission to edit this team.")
        return redirect('team_list')

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated successfully!')
            return redirect('team_list')
    else:
        form = TeamForm(instance=team)
    return render(request, 'planner/team_form.html', {
        'form': form,
        'page_title': f'Edit Team: {team.name}',
        'form_title': 'Edit Team',
        'team': team,
    })

@login_required
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.user not in team.members.all():
        messages.error(request, "You don't have permission to delete this team.")
        return redirect('team_list')

    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Team deleted successfully!')
        return redirect('team_list')
    return render(request, 'planner/team_confirm_delete.html', {
        'object': team,
        'page_title': 'Delete Team',
    })

# ========== Calendar ==========

@login_required
def get_calendar_events(request):
    return JsonResponse(EVENTS, safe=False)

@csrf_exempt
@login_required
def create_calendar_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        EVENTS.append({
            "title": data['title'],
            "start": data['start'],
            "end": data['end']
        })
        return JsonResponse({"status": "created"}, status=201)

@login_required
def calendar_embed_view(request):
    return render(request, 'calendar.html')
