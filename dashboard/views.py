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

class DashboardView(ListView):
    model = Measurement
    template_name = 'dashboard/dashboard_detail.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        userHash = '9d54e1076976a0a287de0dc1c51ae3a23d876556d0dab99' #get_object_or_404(Measurement, userHash=self.kwargs.get('userHash'))
        return Measurement.objects.filter(userHash=userHash).order_by('-timestamp')


def line_chart(request):
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

class MeasurementsDeleteView(DeleteView):
    model = Measurement
    success_url = '/'

    #TODO Implement the function to drop the table