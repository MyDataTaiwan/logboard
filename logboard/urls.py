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
from django.conf.urls import url
from django.urls import path, include
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.records.views import RecordViewSet
from apps.users.views import CustomUserViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="LogBoard API",
        default_version='v1',
        description="Logboard v0.5.0",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="GPL-3.0 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"records", RecordViewSet, "records")
router.register(r"users", CustomUserViewSet, "users")

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api/v1/auth/", include("djoser.urls.authtoken")),
    path("api/v1/", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()

if settings.ADMIN_ENABLED:
    urlpatterns.append(path("admin/", admin.site.urls))
