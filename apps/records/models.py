from django.conf import settings
from django.db import models


class Record(models.Model):
    content = models.TextField()
    content_hash = models.CharField(max_length=255)
    transaction_hash = models.CharField(max_length=255)
    content_verified = models.BooleanField(default=False)
    transaction_verified = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="records", on_delete=models.CASCADE
    )
