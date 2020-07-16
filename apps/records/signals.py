import base64
from datetime import datetime
import json

from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.utils import timezone

from apps.records.models import Record
from apps.mylog.models import MyLog


def parse_record(sender, instance, **kwargs):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    parsed_content = json.loads(instance.content)
    template_name = parsed_content.get("templateName", None)
    app_timestamp = parsed_content.get("timestamp", None)
    timestamp = datetime.fromtimestamp(app_timestamp // 1000)
    proof = parsed_content.get("proof", None)
    owner = instance.owner
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

    fields = parsed_content.get("fields", None)
    photoField = None
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    if fields:
        for idx, field in enumerate(fields):
            if field.get('type', None) == 'photo' and field.get('value', None):
                photoField = fields.pop(idx)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    mylog = MyLog(template_name=template_name, timestamp=timestamp, proof=proof, owner=owner, fields=fields)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    if photoField:
        photoByteString = photoField.get('value', '')
        data = ContentFile(base64.b64decode(photoByteString))
        file_name = "'photo.jpg"
        mylog.photo.save(file_name, data, save=True)
        mylog.save()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


post_save.connect(parse_record, sender=Record, dispatch_uid="parse_record")
