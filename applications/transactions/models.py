import uuid

from django.db import models


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        'user_wallet.UserWallet',
        on_delete=models.CASCADE,
        related_name='transactions',
        to_field='wallet_address',
        )
    recipient = models.ForeignKey(
        'shop_wallet.ShopWallet',
        on_delete=models.CASCADE,
        related_name='transactions',
        to_field='wallet_address',
        )
    transaction_time = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()