# Django Imports
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import JsonResponse

from django.views.generic import(
    ListView,
    DeleteView
)

# Django Restframework imports
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

# Else
import logging
from datetime import datetime,timedelta
from .models import Records

#Create a logger instance
logger = logging.getLogger('__name__')

# TODO filter the irrelevant ones out with queryset filter, get filter argumeent from URL
class ReviewHomeView(ListView):
    model = Records
    template_name = 'dashboard/home.html'
    context_object_name = "records"
    queryset = Records.objects.values('identity').annotate(dcount=Count('identity'))

class DashboardHomeView(ListView):
    model = Records
    template_name = 'dashboard/dashboard_detail.html'
    context_object_name = 'records'

    # TODO: GRAB THE custodian hash (unique URL) from the URL to filter by relevant entries
    custodian_hash = ""

    def get_queryset(self):
        return Records.objects.order_by('timestamp').filter(identity=self.kwargs['userHash'])


class LineChart(APIView):
    # Temperature Constants for verification and line threshhold
    MAX_BODY_TEMP = 42
    CRITICAL_TEMP  = 37.5

    model = Records

    labels = []
    record = []
    threshold = []

# TODO: dig into the content to retrieve body temp
    queryset = Records.objects.values('timestamp','content').order_by('timestamp')
    for entry in queryset:
        labels.append(datetime.fromtimestamp(entry['timestamp']))
        record.append(entry['content']['bodyTemperature'])
        threshold.append(CRITICAL_TEMP)


    def get(self, request, format=None):
        data = {
            "labels": self.labels,
            "record": self.record,
            "threshold": self.threshold
        }   
        return Response(data)


class MapView(APIView):
    model = Records

    labels = []
    latitude = []
    longitude = []

    queryset = Records.objects.values('timestamp','content').order_by('timestamp')
    for entry in queryset:
        labels.append(entry['timestamp'])
        latitude.append(entry['content']['locationStamp']['latitude'])
        longitude.append(entry['content']['locationStamp']['longitude'])

    def get(self, request, format=None):
        data = {
            "labels": self.labels,
            "latitude": self.latitude,
            "longitude": self.longitude
        }   
        return Response(data)


class RecordsDeleteView(DeleteView):
    model = Records
    success_url = '/'

    #TODO Implement the function to drop the table