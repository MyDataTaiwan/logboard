from datetime import datetime
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from sorl.thumbnail import get_thumbnail


def upload_photo_path(instance, filename):
    datetime_str = datetime.now().strftime('%Y/%m/%d/%H/%M/%S')
    return '/'.join(['photos', datetime_str, filename])


def upload_thumbnail_path(instance, filename):
    datetime_str = datetime.now().strftime('%Y/%m/%d/%H/%M/%S')
    return '/'.join(['thumbnails', datetime_str, filename])

class Record(models.Model):
    raw_content = models.TextField()
    transaction_hash = models.CharField(max_length=255, blank=True)
    transaction_hash_validated = models.CharField(max_length=255, default="pending")
    content_hash_verified = models.CharField(max_length=255, default="pending")
    content_parsed = models.CharField(max_length=255, default="pending")
    template_name = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(null=True)
    proof = JSONField(null=True)
    fields = JSONField(null=True)
    photo = models.ImageField(
        upload_to=upload_photo_path,
        blank=True,
    )
    thumbnail = models.ImageField(
        upload_to=upload_thumbnail_path,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="records", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.transaction_hash
    
    def save(self, *args, **kwargs):
        if self.photo:
            self.thumbnail = get_thumbnail(
                self.photo,
                '150x150',
                crop='center',
                quality=99
            ).name
        super(Record, self).save(*args, **kwargs)
