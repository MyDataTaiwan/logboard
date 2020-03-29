from django.shortcuts import render
from django.http import JsonResponse
"""
from rest_framework.views import APIView
from rest_framework.response import Response
"""
from datetime import datetime
import pandas as pd
import requests
from . import models

#Constant for the yellow threshhold line
CRITICAL_TEMP  = 37.5

def home(request):
    monitoring_data = pd.DataFrame(models.load_CID_data())
    context = {
        #TODO 000 check with the DJANGO Template functions how to get nested Values and Format the Timestamps properly
        #TODO 001 Aggregate the days in a dataframe e.g. all timestamps of a specific day get the max temp. and min. temp
        'timestamps': monitoring_data['timestamp'],
        'body_temp': monitoring_data['body_temperature'],
        'body_temp_max': monitoring_data['body_temperature'],
        'body_temp_min': monitoring_data['body_temperature'],
        'coughing': monitoring_data['coughing'],
        'running_nose': monitoring_data['running_nose'],
    }
    return render(request, 'dashboard/dashboard.html', context)

#TODO  003 Fix the display issue with the chart, by implementing the restful API
def population_chart(request):
    monitoring_data = pd.DataFrame(models.load_CID_data())
    monitoring_data['critical_temp'] = CRITICAL_TEMP

    #TODO: 002 Implement the aggregation by day, to find the max and min body_temp of the days
    chart_df = monitoring_data[['timestamp', 'body_temperature', 'critical_temp']]

    data = {
        'timestamps': chart_df['timestamp'],
        'body_temp': chart_df['body_temperature'],
        'body_temp_max': chart_df['body_temperature'],
        'body_temp_min': chart_df['body_temperature'],
        'body_temp_critical': chart_df['critical_temp'],
    }

    return JsonResponse(data)

#TODO: Use Restful API to communicate with the chart as indicated in 003
""" class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        monitoring_data = pd.DataFrame(models.load_CID_data())
        monitoring_data['critical_temp'] = CRITICAL_TEMP

        #TODO: 002 Implement the aggregation by day, to find the max and min body_temp of the days
        chart_df = monitoring_data[['timestamp', 'body_temperature', 'critical_temp']]

        data = {
            'timestamps': chart_df['timestamp'],
            'body_temp': chart_df['body_temperature'],
            'body_temp_max': chart_df['body_temperature'],
            'body_temp_min': chart_df['body_temperature'],
            'body_temp_critical': chart_df['critical_temp'],
        }
        return Response(data) """