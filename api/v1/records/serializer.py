import json
import logging
from rest_framework import serializers

from applications.archives.models import Records


logger = logging.getLogger(__name__)


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            ret['content'] = json.loads(ret['content'].replace('\'', '\"').replace('None', 'null').replace('True', 'true').replace('False', 'false'))
        except Exception as e:
            logger.warning('Failed to parse content JSON. Reason: {}'.format(e))
        return ret
