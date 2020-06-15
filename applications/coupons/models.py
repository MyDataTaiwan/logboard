import uuid

from django.db import models


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    coupon_provider_id = models.UUIDField()
    created_time = models.DateTimeField(auto_now_add=True)
    redeemed_time = models.DateTimeField(null=True, blank=True, editable=False)
    device_id = models.CharField(max_length=255, unique=True)
    redeemed = models.BooleanField(default=False, editable=False)