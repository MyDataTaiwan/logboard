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


class ReviewHomeView(ListView):
    model = Records
    template_name = 'dashboard/home.html'
    context_object_name = "records"
    queryset = Records.objects.values('identity').annotate(dcount=Count('identity'))

    # TODO: in Productive DB it might be better to use this
    #queryset =  Records.objects.order_by('-review_status').distinct('identity')

class DashboardHomeView(ListView):
    model = Records
    template_name = 'dashboard/dashboard_detail.html'
    context_object_name = 'records'
    queryset = Records.objects.order_by('timestamp')


class LineChart(APIView):
    model = Records

    labels = []
    data = []

# TODO: dig into the content to retrieve body temp
    queryset = Records.objects.values('timestamp','review_status','content').order_by('-timestamp')
    for entry in queryset:
        labels.append(entry['timestamp'])
        data.append(entry['review_status'])


    def get(self, request, format=None):
        data = {
            "labels": self.labels,
            "data": self.data,
        }   

        return Response(data)

def map_locations(request):
    latitude = []
    longitude = []

    queryset = Records.objects.order_by('timestamp')
    for measurement in queryset:
        latitude.append(measurement.latitude)
        longitude.append(measurement.longitude)

    return JsonResponse(data={
        'latitude': latitude,
        'longitude': longitude,
    })


class RecordsDeleteView(DeleteView):
    model = Records
    success_url = '/'

    #TODO Implement the function to drop the table