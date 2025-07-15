"""
Development settings for waste_sorter project.
"""

from .base import *

# Debug should be True in development
DEBUG = True

# Allow all hosts for development
ALLOWED_HOSTS = ['*']

# Email backend for development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development database (already configured in base.py)
# You can override database settings here if needed

# Development-specific middleware (add debug toolbar if needed)
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Development-specific apps
# INSTALLED_APPS += ['debug_toolbar']

# Security settings for development
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
