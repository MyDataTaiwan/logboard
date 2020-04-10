from datetime import datetime

from django.db import models
from jsonfield import JSONField


def archive_object_key(instance, filename):
    datetime_str = datetime.now().strftime('%Y/%m/%d/%H/%M/%S')
    return '/'.join([
        'fake_public_key', 'archives', datetime_str, filename
    ])


class Archive(models.Model):
    #id = models.AutoField(primary_key=True)
    file = models.FileField(
        upload_to=archive_object_key, blank='false', null='false')
    file_name = models.CharField(default='untitled_file', max_length=255)
    file_size = models.BigIntegerField(default=0)
    #uploaded_at = models.DateTimeField(auto_now_add=True)
    #data_owner = models.ForeignKey(
    #    'data_owners.DataOwner',
    #    on_delete=models.CASCADE,
    #    related_name='archives',
    #)


# TODO: Replace api/v1/records/ completely.
class Records(models.Model):
    timestamp = models.IntegerField(default=0)
    identity = models.CharField(max_length=50)
    content = JSONField()