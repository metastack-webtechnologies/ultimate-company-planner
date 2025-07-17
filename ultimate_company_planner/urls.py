from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # URL for the Django administration site
    path('', include('planner.urls')), # Include your 'planner' app's URLs at the root
]