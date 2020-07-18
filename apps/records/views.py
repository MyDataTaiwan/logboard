from datetime import datetime
import logging

from django.db import transaction
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.records.models import Record
from apps.records.serializers import RecordSerializer, RecordCreateSerializer
from apps.records.tasks import parse_record


logger = logging.getLogger(__name__)


class RecordViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        return Record.objects.filter(owner=user).order_by('-id')

    def create(self, request):
        serializer = RecordCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            transaction.on_commit(lambda: parse_record.delay(serializer.data['id']))
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
