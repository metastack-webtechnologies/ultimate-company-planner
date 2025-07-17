{% load static %} <!-- Load Django's staticfiles tag to link CSS/JS -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Dynamically set page title from Django views -->
    <title>Ultimate Company Planner - {% block title %}{% endblock %}</title>
    <!-- Link to your custom CSS file -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <!-- Google Fonts for modern typography (Inter) -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>
    <div class="app-container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <a href="{% url 'dashboard' %}" class="app-logo">
                    <i class="fas fa-calendar-check"></i> Ultimate Planner
                </a>
            </div>
            <nav class="sidebar-nav">
                <ul>
                    <!-- Navigation items with dynamic 'active' class based on current URL -->
                    <li class="nav-item {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}">
                        <a href="{% url 'dashboard' %}">
                            <i class="fas fa-home nav-icon"></i> Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#">
                            <i class="fas fa-list-check nav-icon"></i> Tasks
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#">
                            <i class="fas fa-folder-open nav-icon"></i> Projects
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#">
                            <i class="fas fa-users nav-icon"></i> Teams
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#">
                            <i class="fas fa-calendar-alt nav-icon"></i> Calendar
                        </a>
                    </li>
                    <li class="nav-item">
                        <a href="#">
                            <i class="fas fa-microphone-alt nav-icon"></i> Voice Input <!-- Placeholder for AI Voice -->
                        </a>
                    </li>
                    <!-- Add more navigation items here as you develop -->
                </ul>
            </nav>
            <div class="sidebar-footer">
                <div class="user-info">
                    <!-- Display first letter of username as a simple avatar -->
                    <img src="https://via.placeholder.com/30/cccccc/ffffff?text={{ request.user.username|first|upper }}" alt="User Avatar" class="user-avatar">
                    <span>{{ request.user.username }}</span>
                </div>
                <!-- Logout link for the Django admin logout (can be replaced with custom logout) -->
                <a href="{% url 'admin:logout' %}" class="logout-link" title="Logout">
                    <i class="fas fa-sign-out-alt"></i>
                </a>
            </div>
        </aside>

        <main class="main-content">
            <header class="main-header">
                <!-- Display page title from Django views -->
                <h1 class="page-title">{% block page_title %}{% endblock %}</h1>
                <div class="header-actions">
                    <button class="btn btn-primary"><i class="fas fa-plus"></i> Add New</button>
                    <!-- Future: Search bar, notifications, user settings dropdown -->
                </div>
            </header>
            <section class="content-area">
                <!-- Main content for specific pages will be injected here -->
                {% block content %}
                {% endblock %}
            </section>
        </main>
    </div>

    <!-- Link to your main JavaScript file (currently empty) -->
    <script src="{% static 'js/main.js' %}"></script>
    <!-- Allow child templates to add extra JavaScript -->
    {% block extra_js %}{% endblock %}