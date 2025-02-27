"""
URL configuration for production_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('content.urls')),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('payments/', include('payments.urls')),
    path('notifications/', include('notifications.urls')),  # ✅ Notifications URLs
    path('support/', include('support.urls')),  # ✅ Support URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('terms/', TemplateView.as_view(template_name="pages/terms.html"), name='terms'),
    path('team/', TemplateView.as_view(template_name="pages/team.html"), name='team'),
    path('privacy/', TemplateView.as_view(template_name="pages/privacy.html"), name='privacy'),
    path('about/', TemplateView.as_view(template_name="pages/about.html"), name='about'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)