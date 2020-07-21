from datetime import datetime
import logging

from django.core.cache import cache
from django.db import transaction
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.records.models import Record
from apps.records.serializers import RecordSerializer, RecordCreateSerializer
from apps.records.tasks import parse_record
from apps.users.models import CustomUser


logger = logging.getLogger(__name__)


class RecordViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    serializer_class = RecordSerializer

    def get_queryset(self):
        user = self.request.user
        return Record.objects.filter(owner=user).order_by('-id')

    def list(self, request):
        id = request.query_params.get('uid', None)
        no_valid_id_error = {
            'error': 'No valid ID.',
        }
        if not id:
            return Response(no_valid_id_error, status=status.HTTP_400_BAD_REQUEST)
        cache_key = 'record_list_{}'.format(id)
        data = cache.get(cache_key)
        if data:
            return Response(data, status.HTTP_200_OK)
        user = CustomUser.objects.get(pk=id)
        if not user:
            return Response(no_valid_id_error, status=status.HTTP_400_BAD_REQUEST)
        records = Record.objects.filter(owner__id=id).order_by('timestamp')
        serializer = RecordSerializer(records, many=True)
        cache.set(cache_key, serializer.data)
        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cache_key = 'record_retrieve_{}'.format(pk)
        data = cache.get(cache_key)
        if data:
            return Response(data, status.HTTP_200_OK)
        records = self.get_queryset()
        serializer = RecordSerializer(records, many=True)
        cache.set(cache_key, serializer.data)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_anonymous:
            return Response({'detail':'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        cache_key = 'record_list_{}'.format(request.user.id)
        serializer = RecordCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            transaction.on_commit(lambda: parse_record.delay(serializer.data['id']))
            cache.delete(cache_key)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
