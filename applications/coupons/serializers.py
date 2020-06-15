from django.utils import timezone
from rest_framework import serializers

from applications.coupons.models import Coupon
from applications.coupon_providers.models import CouponProvider
from applications.shops.models import Shop


class CouponSerializer(serializers.ModelSerializer):
    coupon_provider = serializers.PrimaryKeyRelatedField(queryset=CouponProvider.objects.all())
    redeemed_shop = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Coupon
        fields = '__all__'

    def create(self, validated_data):
        coupon_provider = validated_data['coupon_provider']
        coupon_provider.quantity -= 1
        coupon_provider.save()
        return Coupon.objects.create(**validated_data)

    def validate(self, data):
        provider = data['coupon_provider']
        if provider.quantity <= 0:
            raise serializers.ValidationError('No remaining quantity for the coupon provider')
        if timezone.now() >= provider.expiration_time:
            raise serializers.ValidationError('The coupon provider has expired')

        return data


class CouponRedeemSerializer(serializers.Serializer):
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all())
    def create(self, validated_data):
        instance = Coupon.objects.get(pk=validated_data['coupon_id'])
        instance.redeemed = True
        instance.redeemed_shop = validated_data['shop']
        instance.redeemed_time = timezone.now()
        instance.save()
        return instance

    def validate(self, data):
        coupon = self.context.get('coupon')
        if coupon.redeemed:
            raise serializers.ValidationError('Coupon has already been redeemed')
        # Do other validations here
        data['coupon_id'] = coupon.id
        return data