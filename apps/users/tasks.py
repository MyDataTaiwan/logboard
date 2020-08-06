from datetime import datetime, timedelta

from celery import shared_task
from celery.utils.log import get_task_logger

from apps.users.models import CustomUser


logger = get_task_logger(__name__)


@shared_task
def delete_old_users():
    time_threshold = datetime.now() - timedelta(days=3)
    users = CustomUser.objects.filter(created_at__lte=time_threshold)
    logger.warning('time threshold: {}'.format(time_threshold))
    delete_count = users.count()
    users.delete()
    logger.info('Delete {} users created 3 days ago'.format(delete_count))
