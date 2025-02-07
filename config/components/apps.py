INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'debug_toolbar',
    'rest_framework',
    'rest_framework_simplejwt',
    
    # local apps
    'booking.apps.BookingConfig',
    'users.apps.UsersConfig',
]