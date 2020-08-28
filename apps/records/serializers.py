import logging

from rest_framework import serializers
from apps.records.models import Record
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField


logger = logging.getLogger(__name__)


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'id',
            'raw_content',
            'transaction_hash_validated',
            'content_hash_verified',
            'content_parsed',
            'template_name',
            'timestamp',
            'proof',
            'fields',
            'photo',
            #'thumbnail',
            'owner',
        ]
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
            #'thumbnail',
            'owner',
        ]

    raw_content = serializers.CharField(write_only=True)
    '''
    thumbnail = HyperlinkedSorlImageField(
        '128x128',
        options={"crop": "center"},
        source='photo',
        read_only=True,
    )
    '''


class RecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'raw_content', 'transaction_hash', 'template_name','owner']
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(RecordCreateSerializer, self).create(validated_data)
