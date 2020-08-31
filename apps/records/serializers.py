import logging

from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from apps.records.models import Record
from utils.data_template import DataTemplate


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
            'thumbnail',
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
            'thumbnail',
            'owner',
        ]

    raw_content = serializers.CharField(write_only=True)


class RecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'raw_content', 'transaction_hash', 'template_name','owner']
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super(RecordCreateSerializer, self).create(validated_data)


class TemplateSerializer(serializers.Serializer):
    template = serializers.CharField(write_only=True)
    
    def to_internal_value(self, data):
        template_name = data.get('template')
        data_template = DataTemplate(template_name)
        if not data_template.template:
            raise serializers.ValidationError({'template': 'not a valid template name'})
        return {
            'template': data_template.template,
        }
    
    def to_representation(self, instance):
        return instance['template']