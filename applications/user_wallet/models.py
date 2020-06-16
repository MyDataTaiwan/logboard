import uuid

from django.db import models


class UserWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_address = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='active')
    current_balance = models.IntegerField(default=0, editable=False)
    accumulated_redeem_balance = models.IntegerField(default=0, editable=False)