from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class Record(models.Model):
    raw_content = models.TextField()
    transaction_hash = models.CharField(max_length=255)
    transaction_hash_validated = models.CharField(max_length=255, default="pending")
    content_hash_verified = models.CharField(max_length=255, default="pending")
    content_parsed = models.CharField(max_length=255, default="pending")
    template_name = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(null=True)
    proof = JSONField(null=True)
    fields = JSONField(null=True)
    photo = models.ImageField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="records", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.transaction_hash
