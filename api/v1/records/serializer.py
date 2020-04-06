from rest_framework import serializers

from api.v1.records.models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
