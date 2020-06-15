from django.shortcuts import render
from rest_framework import viewsets

from applications.coupon_providers.models import CouponProvider
from applications.coupon_providers.serializers import CouponProviderSerializer


class CouponProviderViewSet(viewsets.ModelViewSet):
    serializer_class = CouponProviderSerializer
    queryset = CouponProvider.objects.all()