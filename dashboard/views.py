from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import(
    ListView,
    DetailView,
    TemplateView,
    DeleteView
)

from datetime import datetime
import pandas as pd
import requests, logging
from .models import Measurement, AuthCustodianHashes

#Create a logger instance
logger = logging.getLogger('views')

class DashboardHomeView(ListView):
    model = AuthCustodianHashes
    template_name = 'dashboard/home.html'
    context_object_name = 'hashes'

class DashboardDetailView(DetailView):
    model = Measurement

    def line_chart(self, request):
        labels = []
        body_temperature = []
        body_temperature_MAX = []
        body_temperature_MIN = []
        body_temperature_CRITICAL = []

        queryset = Measurement.objects.order_by('timestamp')

        for measurement in queryset:
            labels.append(measurement.timestamp)
            body_temperature.append(measurement.bodyTemperature)
            body_temperature_MAX.append(measurement.bodyTemperatureMAX)
            body_temperature_MIN.append(measurement.bodyTemperatureMIN)
            body_temperature_CRITICAL.append(measurement.bodyTemperatureCRITICAL)

        return JsonResponse(data={
            'labels': labels,
            'body_temperature': body_temperature,
            'body_temperature_MAX': body_temperature_MAX,
            'body_temperature_MIN': body_temperature_MIN,
            'body_temperature_CRITICAL': body_temperature_CRITICAL,

        })

    def map_locations(self, request):
        latitude = []
        longitude = []

        queryset = Measurement.objects.order_by('timestamp')
        for measurement in queryset:
            latitude.append(measurement.latitude)
            longitude.append(measurement.longitude)

        return JsonResponse(data={
            'latitude': latitude,
            'longitude': longitude,
        })


    class MeasurementsDeleteView(DeleteView):
        model = Measurement
        success_url = '/'

        #TODO Implement the function to drop the table