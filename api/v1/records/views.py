from django.shortcuts import render
from rest_framework import viewsets

from api.v1.records.models import Record
from api.v1.records.serializer import RecordSerializer


# ViewSets define the view behavior.
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
