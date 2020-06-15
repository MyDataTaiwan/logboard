import uuid

from django.db import models


class CouponProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    name = models.CharField(max_length=255)
    discount = models.IntegerField(default=20)
    quantity = models.IntegerField()
    expiration_time = models.DateTimeField()