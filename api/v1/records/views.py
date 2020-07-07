from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from applications.archives.models import Records
from api.v1.records.serializer import RecordSerializer


# ViewSets define the view behavior.
class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer

    def get_queryset(self):
        queryset = Records.objects.all()
        uuid = self.request.query_params.get('uuid', None)
        if uuid is not None:
            queryset = queryset.filter(identity=uuid)
        return queryset
