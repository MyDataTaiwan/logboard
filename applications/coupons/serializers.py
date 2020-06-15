from django.utils import timezone
from rest_framework import serializers

from applications.coupons.models import Coupon
from applications.coupon_providers.models import CouponProvider


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'coupon_provider_id', 'device_id', 'created_time', 'redeemed', 'redeemed_time']

    def create(self, validated_data):
        coupon_provider = CouponProvider.objects.get(pk=validated_data['coupon_provider_id'])
        coupon_provider.quantity -= 1
        coupon_provider.save()
        return Coupon.objects.create(**validated_data)

    def validate(self, data):
        if not CouponProvider.objects.filter(pk=data['coupon_provider_id']).exists():
            raise serializers.ValidationError('matching coupon_provider_id does not exist')

        provider = CouponProvider.objects.get(pk=data['coupon_provider_id'])
        if provider.quantity <= 0:
            raise serializers.ValidationError('No remaining quantity for the coupon provider')
        if timezone.now() >= provider.expiration_time:
            raise serializers.ValidationError('The coupon provider has expired')

        return data


class CouponRedeemSerializer(serializers.Serializer):
    def create(self, validated_data):
        instance = Coupon.objects.get(pk=validated_data['coupon_id'])
        instance.redeemed = True
        instance.redeemed_time = timezone.now()
        instance.save()
        return instance

    def validate(self, data):
        coupon = self.context.get('coupon')
        if coupon.redeemed == True:
            raise serializers.ValidationError('Coupon has already been redeemed')
        # Do other validations here
        data['coupon_id'] = coupon.id
        return data