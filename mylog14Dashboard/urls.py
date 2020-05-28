"""mylog14Dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers, viewsets

from api.v1.records.views import RecordViewSet
from api.v1.archive_viewset import ArchiveViewset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'records', RecordViewSet, basename='Record')
router.register(r'archives', ArchiveViewset, 'archives')

urlpatterns = [
    path('dashboard/', include('applications.archives.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
]
if settings.ADMIN_ENABLED:
    urlpatterns.append(path('admin/', admin.site.urls))