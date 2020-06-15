from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.coupons.models import Coupon
from applications.coupons.serializers import CouponSerializer, CouponRedeemSerializer


class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()

    @action(detail=True, methods=['post'])
    def redeem(self, request, pk=None):
        coupon = self.get_object()
        serializer = CouponRedeemSerializer(data=request.data, context={'coupon': coupon})
        if serializer.is_valid():
            serializer.save()
            coupon_serializer = CouponSerializer(serializer.instance)
            return Response(coupon_serializer.data, status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)