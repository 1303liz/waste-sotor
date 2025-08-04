"""
URL configuration for waste_sorter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recycle/', include('recycle_tips.urls', namespace='recycle_tips')),
    path('waste/', include('waste_logs.urls', namespace='waste_logs')),
    path('accounts/', include('accounts.urls')),
    path('', include('dashboard.urls')),  # Dashboard app is now the homepage
    # Add a direct path to the dashboard
    path('dashboard/', include('dashboard.urls')),
    # Handle favicon.ico requests to prevent 404 errors after login
    path('favicon.ico', RedirectView.as_view(url='/dashboard/')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Add django_browser_reload URLs for Tailwind development (Disabled to prevent ping messages)
    # urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
    
    # Add debug toolbar URLs in development
    try:
        import debug_toolbar
        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass
