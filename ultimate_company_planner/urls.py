from django.contrib import admin
from django.urls import path, include
from planner.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('planner.urls')),
    path('accounts/', include('allauth.urls')),  # Use allauth URLs
    path('accounts/signup/', signup_view, name='signup'),  # Optional: if overriding default
]
