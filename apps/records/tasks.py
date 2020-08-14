import base64
from datetime import datetime
import hashlib
import json

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.utils.timezone import make_aware
from django.core.files.base import ContentFile
from niota import niota

from apps.records.models import Record


logger = get_task_logger(__name__)


def _get_iota_content_hash(transaction_hash):
    client = niota.NumbersIOTA(logger)
    transaction = client.get_transaction(transaction_hash)
    message = client.get_message(transaction)["message"]
    return message.get("hash", None)


def _invalidate_record_cache(owner_id):
    list_cache_key = 'record_list_{}'.format(owner_id)
    cache.delete(list_cache_key)


@shared_task
def parse_record(pk):
    SUCCESS = "success"
    FAILURE = "failure"
    instance = Record.objects.get(pk=pk)

    # Validate transaction_hash and get content hash on ledger
    iota_content_hash = None
    try:
        iota_content_hash = _get_iota_content_hash(instance.transaction_hash)
        instance.transaction_hash_validated = SUCCESS
    except Exception as error:
        logger.error(error)
        instance.transaction_hash_validated = FAILURE

    # Verify content hash
    content_hash = hashlib.sha256(instance.raw_content.encode("utf-8")).hexdigest()
    if content_hash == iota_content_hash:
        instance.content_hash_verified = SUCCESS
    else:
        logger.warning('Record id={} failed content hash verification'.format(pk))
        instance.content_hash_verified = FAILURE

    try:
        parsed_content = json.loads(instance.raw_content)
        instance.content_parsed = SUCCESS
    except Exception as error:
        logger.error(error)
        instance.content_parsed = FAILURE
    if instance.content_parsed == SUCCESS:
        app_timestamp = parsed_content.get("timestamp", None)
        if app_timestamp:
            instance.timestamp = make_aware(datetime.fromtimestamp(app_timestamp // 1000))
        instance.proof = parsed_content.get("proof", None)
        instance.fields = parsed_content.get("fields", None)
        photoByteString = None
        if instance.fields:
            for idx, field in enumerate(instance.fields):
                if field.get('name', None) == 'photo' and field.get('value', None):
                    photoField = instance.fields.pop(idx)
                    photoByteString = photoField.get('value', None)
                    break
        if photoByteString:
            data = ContentFile(base64.b64decode(photoByteString))
            file_name = "{}/{}.jpg".format(instance.owner.id, content_hash)
            instance.photo.save(file_name, data, save=True)
    _invalidate_record_cache(instance.owner.id)
    instance.save()
