import hashlib
import json
import logging

from rest_framework import serializers
from apps.records.models import Record
from apps.users.models import CustomUser


logger = logging.getLogger(__name__)


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = [
            'id',
            'transaction_hash_validated',
            'content_hash_verified',
            'content_parsed',
            'template_name',
            'timestamp',
            'proof',
            'fields',
            'photo',
            'owner',
        ]

    raw_content = serializers.CharField(write_only=True)


class RecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'raw_content', 'transaction_hash', 'owner']
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(RecordCreateSerializer, self).create(validated_data)
