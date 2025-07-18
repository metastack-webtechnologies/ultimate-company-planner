from django.contrib import admin
from .models import Team, Project, Task

# Register your models here so they appear in the Django administration interface
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Task)
