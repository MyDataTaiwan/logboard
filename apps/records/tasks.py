import base64
from datetime import datetime
import json

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.records.models import Record
from apps.mylog.models import MyLog


logger = get_task_logger(__name__)


@shared_task
def parse_record(pk):
    instance = Record.objects.get(pk=pk)
    parsed_content = json.loads(instance.content)
    template_name = parsed_content.get("templateName", None)
    app_timestamp = parsed_content.get("timestamp", None)
    timestamp = datetime.fromtimestamp(app_timestamp // 1000)
    proof = parsed_content.get("proof", None)
    owner = instance.owner
    record = instance

    fields = parsed_content.get("fields", None)
    photoField = None
    if fields:
        for idx, field in enumerate(fields):
            if field.get('type', None) == 'photo' and field.get('value', None):
                photoField = fields.pop(idx)
    mylog = MyLog(template_name=template_name, timestamp=timestamp, proof=proof, owner=owner, fields=fields, record=record)
    if photoField:
        photoByteString = photoField.get('value', '')
        data = ContentFile(base64.b64decode(photoByteString))
        file_name = "'photo.jpg"
        mylog.photo.save(file_name, data, save=True)
        mylog.save()