import json
import logging

from rest_framework import serializers
from apps.mylog.models import MyLog
from apps.users.models import CustomUser


logger = logging.getLogger(__name__)


class MyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyLog
        fields = "__all__"

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super(MyLogSerializer, self).create(validated_data)
