from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.records.models import Record

class MyLog(models.Model):
    template_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    proof = JSONField()
    fields = JSONField()
    photo = models.ImageField(null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="mylogs", on_delete=models.CASCADE
    )
    record = models.OneToOneField(
        Record,
        related_name='mylog',
        on_delete=models.CASCADE,
    )   