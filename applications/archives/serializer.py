import logging

from rest_framework import serializers
from django_celery_results.models import TaskResult
from applications.archives.models import Archive
from applications.archives.validators import validate_file_extension
#from applications.data_owners.models import DataOwner
#from applications.data_owners.serializer import DataOwnerSerializer

logger = logging.getLogger(__name__)


class ParserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ['task_id', 'id', 'status']


class ArchiveSerializer(serializers.Serializer):
    #id = serializers.IntegerField(read_only=True)
    file = serializers.FileField(max_length=255,
            validators=[validate_file_extension])
    file_name = serializers.CharField(read_only=True)
    file_size = serializers.IntegerField(read_only=True)
    #uploaded_at = serializers.DateTimeField(read_only=True)
    #data_owner = serializers.SlugRelatedField(
    #    slug_field = 'public_key',
    #    queryset = DataOwner.objects.all()
    #)

    def create(self, obj):
        obj['file_name'] = obj['file'].name
        obj['file_size'] = obj['file'].size
        return Archive.objects.create(**obj)
