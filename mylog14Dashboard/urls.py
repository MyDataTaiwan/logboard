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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from rest_framework import permissions, routers, viewsets
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from api.v1.records.views import RecordViewSet
from api.v1.archive_viewset import ArchiveViewset
from applications.shops.views import ShopViewSet
from applications.coupons.views import CouponViewSet
from applications.coupon_providers.views import CouponProviderViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'records', RecordViewSet, basename='Record')
router.register(r'archives', ArchiveViewset, 'archives')
router.register(r'shops', ShopViewSet, 'shops')
router.register(r'coupons', CouponViewSet, 'coupons')
router.register(r'coupon_providers', CouponProviderViewSet, 'coupon_providers')

urlpatterns = [
    path('dashboard/', include('applications.archives.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += staticfiles_urlpatterns()

if settings.ADMIN_ENABLED:
    urlpatterns.append(path('admin/', admin.site.urls))
