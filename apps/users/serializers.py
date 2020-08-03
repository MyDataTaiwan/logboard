import json
import logging
import os

from rest_framework import serializers
from apps.users.models import CustomUser


logger = logging.getLogger(__name__)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user
