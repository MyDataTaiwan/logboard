from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import(
    ListView,
    DetailView,
    DeleteView
)

from datetime import datetime
import pandas as pd
import requests, logging
from .models import Measurement


#Create a logger instance
logger = logging.getLogger('views')



class DashboardHomeView(ListView):
    model = Measurement
    template_name = 'dashboard/home.html'
    context_object_name = 'measurements'

class DashboardView(ListView):
    model = Measurement
    template_name = 'dashboard/dashboard_detail.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        userHash = 'test_hash'
        return Measurement.objects.filter(userHash = userHash).order_by('timestamp')


class LineChartView(DetailView):
    model = Measurement
    context_object_name = 'measurements'

    logger.info(f'Chart was loaded: {context_object_name}')

class MeasurementsDeleteView(DeleteView):
    model = Measurement
    success_url = '/'

    #TODO Implement the function to drop the table
