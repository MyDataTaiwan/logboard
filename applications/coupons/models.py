import uuid

from django.db import models


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    created_time = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=255, unique=True)
    redeemed = models.BooleanField(default=False, editable=False)
    redeemed_time = models.DateTimeField(null=True, blank=True, editable=False)
    coupon_provider = models.ForeignKey(
        'coupon_providers.CouponProvider',
        on_delete=models.CASCADE,
        related_name='coupon',
        )
    redeemed_shop = models.ForeignKey(
        'shops.Shop',
        on_delete=models.CASCADE,
        related_name='coupon',
        blank=True,
        null=True,
        )