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

    def get(self, request, *args, **kwargs):
        print(self.kwargs)
        data = {
            'records': self.get_queryset(),
            'userHash': self.kwargs['userHash'],
        }
        return render(request=request, template_name=self.template_name, context=data)

# TODO
class DataView(APIView):
    # Temperature Constants for verification and line threshhold
    MAX_BODY_TEMP = 41
    CRITICAL_TEMP  = 38

    model = Records

    def get_queryset(self):
        return Records.objects.values('identity', 'timestamp','content').order_by('timestamp')

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



    def get(self, request, userHash=None):
        self.labels = []
        self.record = []
        self.threshold = []
        self.dead = []
        self.latitude = []
        self.longitude = []


        for entry in self.get_queryset().filter(identity=userHash):
            print(entry['timestamp'])
            if entry['content'].get('bodyTemperature', None) != None:
                self.labels.append(datetime.fromtimestamp(entry['timestamp']))
                self.record.append(entry['content']['bodyTemperature'])
                self.threshold.append(self.CRITICAL_TEMP)
                self.dead.append(self.MAX_BODY_TEMP)

                #To move these to the proper place once tested.
                self.latitude.append(entry['content']['locationStamp']['latitude'])
                self.longitude.append(entry['content']['locationStamp']['longitude'])

        data = {
            "labels": self.labels,
            "record": self.record,
            "threshold": self.threshold,
            "dead": self.dead,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
        print(data)
        return Response(data)


class RecordsDeleteView(DeleteView):
    model = Records
    success_url = '/'

    #TODO Implement the function to drop the table
