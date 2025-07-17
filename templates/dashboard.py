{% extends 'base.html' %} {# Inherit from the base layout template #}
{% load static %}

{% block title %}Dashboard{% endblock %} {# Set page title #}
{% block page_title %}Dashboard{% endblock %} {# Set header title #}

{% block content %}
    <div class="welcome-section">
        <h2>Welcome back, {{ username }}!</h2>
        <p>This is your daily overview. Get ready to plan your tasks and collaborate effectively.</p>
        <div class="dashboard-widgets">
            <div class="widget">
                <h3>Today's Focus</h3>
                <p>No major focus set yet. Define your top priority!</p>
                <button class="btn btn-secondary"><i class="fas fa-pencil-alt"></i> Set Focus</button>
            </div>
            <div class="widget">
                <h3>Upcoming Tasks</h3>
                <ul class="task-list">
                    <li><i class="fas fa-circle-check"></i> Project Meeting - Tomorrow</li>
                    <li><i class="fas fa-circle-check"></i> Finalize Report - Friday</li>
                </ul>
                <a href="#" class="view-all">View All Tasks</a>
            </div>
            <div class="widget">
                <h3>Team Activity</h3>
                <p>No new activity.</p>
                <a href="#" class="view-all">View Activity Log</a>
            </div>
            {# Add more widgets here as you develop #}
        </div>
    </div>
{% endblock %}

{% block extra_js %}
    <script>
        // Any dashboard-specific JavaScript can go here.
        // Example: logic to fetch and display dynamic content, or handle interactive elements.
    </script>
{% endblock %}