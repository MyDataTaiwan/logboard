from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from applications.coupon_providers.models import CouponProvider
from applications.coupon_providers.serializers import CouponProviderSerializer, CouponProviderDetailSerializer


class CouponProviderViewSet(viewsets.ModelViewSet):
    serializer_class = CouponProviderSerializer
    queryset = CouponProvider.objects.all()

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = CouponProviderDetailSerializer(instance)
        return Response(serializer.data)