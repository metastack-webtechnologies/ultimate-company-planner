from django.urls import path
from . import views # Import views from the current app (planner)

urlpatterns = [
    # The root URL of the 'planner' app will map to the dashboard view
    # name='dashboard' allows you to refer to this URL by name in templates (e.g., {% url 'dashboard' %})
    path('', views.dashboard_view, name='dashboard'),
    # As you build out features, you'll add more URL patterns here
    # Example: path('tasks/', views.task_list_view, name='task_list'),
    # Example: path('projects/<int:pk>/', views.project_detail_view, name='project_detail'),
]