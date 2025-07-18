from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login # Import login function
from .models import Task, Project, Team
from .forms import TaskForm, ProjectForm, TeamForm, UserCreationForm # Import your forms, including new UserCreationForm

@login_required
def dashboard_view(request):
    # Fetch some data for the dashboard
    user_tasks = Task.objects.filter(assigned_to=request.user, status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS]).order_by('due_date')[:5]
    recent_projects = Project.objects.filter(created_by=request.user).order_by('-created_at')[:3]
    
    context = {
        'username': request.user.username,
        'page_title': 'Dashboard',
        'user_tasks': user_tasks,
        'recent_projects': recent_projects,
    }
    return render(request, 'dashboard.html', context)

# --- User Authentication Views --- # ADDED
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after registration
            messages.success(request, 'Account created successfully! Welcome!')
            return redirect('dashboard')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = UserCreationForm()
    context = {
        'form': form,
        'page_title': 'Sign Up',
        'form_title': 'Create Your Account',
    }
    return render(request, 'registration/signup.html', context)


# --- Task Views ---
@login_required
def task_list(request):
    # Filter tasks based on user (e.g., assigned to user or created by user)
    tasks = Task.objects.filter(assigned_to=request.user).order_by('status', 'due_date') # Or .filter(Q(assigned_to=request.user) | Q(created_by=request.user)).distinct()
    context = {
        'tasks': tasks,
        'page_title': 'All Tasks',
    }
    return render(request, 'planner/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user # Set the creator
            task.save()
            form.save_m2m() # Save ManyToMany relations (like assigned_to)
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    context = {
        'form': form,
        'page_title': 'Create New Task',
        'form_title': 'Create Task',
    }
    return render(request, 'planner/task_form.html', context)

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # Ensure only creator or assigned user can update (add more robust permissions later)
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
    context = {
        'form': form,
        'page_title': f'Edit Task: {task.name}',
        'form_title': 'Edit Task',
        'task': task, # Pass task object for context in template
    }
    return render(request, 'planner/task_form.html', context)

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # Ensure only creator can delete
    if request.user != task.created_by:
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    context = {
        'object': task,
        'page_title': 'Delete Task',
    }
    return render(request, 'planner/task_confirm_delete.html', context)

# --- Project Views ---
@login_required
def project_list(request):
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at') # Or filter by team membership
    context = {
        'projects': projects,
        'page_title': 'All Projects',
    }
    return render(request, 'planner/project_list.html', context)

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
    context = {
        'form': form,
        'page_title': 'Create New Project',
        'form_title': 'Create Project',
    }
    return render(request, 'planner/project_form.html', context)

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
    context = {
        'form': form,
        'page_title': f'Edit Project: {project.name}',
        'form_title': 'Edit Project',
        'project': project,
    }
    return render(request, 'planner/project_form.html', context)

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
    context = {
        'object': project,
        'page_title': 'Delete Project',
    }
    return render(request, 'planner/project_confirm_delete.html', context)

# --- Team Views ---
@login_required
def team_list(request):
    # List teams where the current user is a member
    teams = Team.objects.filter(members=request.user).distinct().order_by('name')
    context = {
        'teams': teams,
        'page_title': 'All Teams',
    }
    return render(request, 'planner/team_list.html', context)

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            # Automatically add the creator to the team members
            team.members.add(request.user)
            messages.success(request, 'Team created successfully!')
            return redirect('team_list')
    else:
        form = TeamForm()
    context = {
        'form': form,
        'page_title': 'Create New Team',
        'form_title': 'Create Team',
    }
    return render(request, 'planner/team_form.html', context)

@login_required
def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    # Only allow team members to update the team (or specific admin roles)
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
    context = {
        'form': form,
        'page_title': f'Edit Team: {team.name}',
        'form_title': 'Edit Team',
        'team': team,
    }
    return render(request, 'planner/team_form.html', context)

@login_required
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    # Only allow a user who is a member to delete the team (or specific admin roles)
    if request.user not in team.members.all():
        messages.error(request, "You don't have permission to delete this team.")
        return redirect('team_list')

    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Team deleted successfully!')
        return redirect('team_list')
    context = {
        'object': team,
        'page_title': 'Delete Team',
    }
    return render(request, 'planner/team_confirm_delete.html', context)
