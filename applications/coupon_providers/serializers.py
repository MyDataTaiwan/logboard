from rest_framework import serializers

from applications.coupon_providers.models import CouponProvider


class CouponProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponProvider
        fields = ['id', 'name', 'discount', 'quantity', 'expiration_time']


class CouponProviderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponProvider
        fields = ['id', 'name', 'discount', 'quantity', 'expiration_time', 'coupon']