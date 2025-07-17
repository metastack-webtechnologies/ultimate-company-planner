import os
import dj_database_url # Import for parsing DATABASE_URL from environment

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable for production, fallback to a default for development
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_insecure_default_secret_key_for_dev_ONLY_CHANGE_THIS_IN_PROD')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG is set via an environment variable, defaulting to True for development
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS allows all hosts for development. In production, list your domain(s).
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'planner', # Your custom app for the planner features
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ultimate_company_planner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS specifies the path to your global templates directory
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True, # Allows Django to find templates within each app's 'templates' folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ultimate_company_planner.wsgi.application'

# Database configuration for PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        # Default database URL, using the Docker service name 'db' as the hostname
        default='postgres://admin:password@db:5432/company_planner_db',
        conn_max_age=600 # Max age of database connections in seconds
    )
}

# Password validation (Django defaults for security)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # Set this to your local timezone, e.g., 'America/New_York'
USE_I18N = True # Enable Django's internationalization system
USE_TZ = True # Enable timezone support

# Static files (CSS, JavaScript, Images) configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Path to your global static directory
]

# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
