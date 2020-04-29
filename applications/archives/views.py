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
    template_name = 'dashboard/dashboard_detail2.html'
    context_object_name = 'records'

    def get_queryset(self):
        return Records.objects.order_by('timestamp').filter(identity=self.kwargs['userHash'])

# TODO
class DataView(APIView):
    # Temperature Constants for verification and line threshhold
    MAX_BODY_TEMP = 40
    CRITICAL_TEMP  = 38

    model = Records

    labels = []
    record = []
    threshold = []
    dead = []
    latitude = []
    longitude = []

    # Hardcoded for debug purpose TODO clean code here,
    def custodian_hash(self):
        custodian_hash = '8fa4a4f6-4827-4c3d-8e1e-cf548e48b988'
        return custodian_hash

    queryset = Records.objects.values('identity', 'timestamp','content').order_by('timestamp')

    for entry in queryset:
        if entry['content'].get('bodyTemperature', None) != None:
            # App (Javascript) uses 13-digit timestamp (msecs),
            # so we convert it to 10-digit Unix time timestamp (secs) for Python.
            digits = len(str(entry['timestamp']))
            if digits == 10:
                unix_time_timestamp = entry['timestamp']
            if digits == 13:
                unix_time_timestamp = entry['timestamp'] / 1000
            if digits == 16:
                unix_time_timestamp = entry['timestamp'] / 1000000
            else:
                logger.warn(
                    'Timestamp {0} has unknown digits {1}'
                    ', keep using it and the following codes might has some issues.'
                    ''.format(entry['timestamp'], digits)
                )
                unix_time_timestamp = entry['timestamp']
            labels.append(datetime.fromtimestamp(unix_time_timestamp))
            record.append(entry['content']['bodyTemperature'])
            threshold.append(CRITICAL_TEMP)
            dead.append(MAX_BODY_TEMP)

            #To move these to the proper place once tested.
            latitude.append(entry['content']['locationStamp']['latitude'])
            longitude.append(entry['content']['locationStamp']['longitude'])

    def get(self, request, format=None):

        data = {
            "labels": self.labels,
            "record": self.record,
            "threshold": self.threshold,
            "dead": self.dead,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
        return Response(data)


class RecordsDeleteView(DeleteView):
    model = Records
    success_url = '/'

    #TODO Implement the function to drop the table
