from rest_framework import serializers

from applications.archives.models import Records

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'
