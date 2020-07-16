"""logboard URL Configuration

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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers, viewsets
from rest_framework.authtoken import views

from apps.records.views import RecordViewSet
from apps.users.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r"records", RecordViewSet, "records")
router.register(r"users", CustomUserViewSet, "users")

urlpatterns = [
    path("api/v1/auth/", include("djoser.urls.authtoken")),
    path("api/v1/", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()

if settings.ADMIN_ENABLED:
    urlpatterns.append(path("admin/", admin.site.urls))
