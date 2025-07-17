from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Decorator to ensure user is logged in

@login_required # This decorator ensures that only authenticated users can access this view
def dashboard_view(request):
    # In a fully developed app, this view would fetch and prepare
    # user-specific tasks, projects, daily focus items, etc., from the database.
    # For now, it simply renders the basic dashboard template.
    context = {
        'username': request.user.username, # Pass the logged-in username to the template
        'page_title': 'Dashboard' # Title to be displayed on the page
    }
    return render(request, 'dashboard.html', context)

