import logging

from django.core.files.base import ContentFile
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.models import CustomUser
from apps.users.serializers import CustomUserSerializer
from apps.users.permissions import IsCreationOrIsAuthenticated


logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCreationOrIsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(id=user.id)
