from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model for authentication

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Many-to-Many relationship with User, allowing multiple users in a team
    # related_name='teams' allows User objects to access their teams via user.teams.all()
    members = models.ManyToManyField(User, related_name='teams', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # Correct plural name for the admin interface
        verbose_name_plural = "Teams"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) # Description is optional
    # ForeignKey to Team, allowing a project to be associated with a team (optional)
    # on_delete=models.SET_NULL means if a team is deleted, its projects' team field becomes NULL
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    # ForeignKey to User, indicating who created the project
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set creation timestamp
    updated_at = models.DateTimeField(auto_now=True) # Automatically updated on each save

    def __str__(self):
        return self.name

class Task(models.Model):
    # Choices for task priority
    class Priority(models.TextChoices):
        HIGH = 'HI', 'High'
        MEDIUM = 'ME', 'Medium'
        LOW = 'LO', 'Low'

    # Choices for task status
    class Status(models.TextChoices):
        TODO = 'TD', 'To Do'
        IN_PROGRESS = 'IP', 'In Progress'
        BLOCKED = 'BL', 'Blocked'
        COMPLETED = 'CO', 'Completed'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # ForeignKey to Project, allowing a task to belong to a project (optional)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    # Many-to-Many relationship with User, allowing a task to be assigned to multiple users
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=2, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.TODO)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_time_minutes = models.IntegerField(blank=True, null=True, help_text="Estimated time to complete in minutes")

    def __str__(self):
        return self.name

    class Meta:
        # Default ordering for tasks: by due date (ascending), then by priority
        ordering = ['due_date', 'priority']
        verbose_name_plural = "Tasks"


