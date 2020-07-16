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
        fields = [
            "id",
            "content",
            "content_hash",
            "transaction_hash",
            "content_verified",
            "transaction_verified",
            "owner",
        ]
        read_only_fields = ["id", "content_verified", "transaction_verified", "owner"]

    def create(self, validated_data):
        hs = hashlib.sha256(validated_data["content"].encode("utf-8")).hexdigest()
        print(hs)
        validated_data["owner"] = self.context["request"].user
        return super(RecordSerializer, self).create(validated_data)
