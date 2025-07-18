from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm # Import Django's default UserCreationForm
from .models import Task, Project, Team

# Custom User Creation Form for registration
class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta(DjangoUserCreationForm.Meta):
        model = DjangoUserCreationForm.Meta.model
        fields = DjangoUserCreationForm.Meta.fields + ('email',) # Add email to the fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS classes to form fields
        for field_name in self.fields:
            if field_name == 'email':
                self.fields[field_name].widget.attrs.update({'class': 'form-input'})
            elif field_name == 'username':
                self.fields[field_name].widget.attrs.update({'class': 'form-input'})
            elif 'password' in field_name:
                self.fields[field_name].widget.attrs.update({'class': 'form-input'})


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'project', 'assigned_to', 'due_date', 'priority', 'status', 'estimated_time_minutes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'estimated_time_minutes': forms.NumberInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'name': 'Task Name',
            'description': 'Description',
            'project': 'Project',
            'assigned_to': 'Assign To',
            'due_date': 'Due Date',
            'priority': 'Priority',
            'status': 'Status',
            'estimated_time_minutes': 'Estimated Time (minutes)',
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'team']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
            'team': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Project Name',
            'description': 'Description',
            'team': 'Team',
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
        }
        labels = {
            'name': 'Team Name',
            'members': 'Team Members',
        }
