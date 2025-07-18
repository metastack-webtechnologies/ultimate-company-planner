from django.contrib import admin
from django.urls import path, include
from planner.views import signup_view # Import your custom signup view

urlpatterns = [
    path('admin/', admin.site.urls), # URL for the Django administration site
    path('', include('planner.urls')), # Include your 'planner' app's URLs at the root
    
    # ADDED: Django authentication URLs
    path('accounts/', include('django.contrib.auth.urls')), # Provides login, logout, password reset, etc.
    path('accounts/signup/', signup_view, name='signup'), # Your custom signup URL
]
