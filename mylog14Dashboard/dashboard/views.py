from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import requests

def get_data():
    #Dummy Data to be replaced
    monitoring_data = [
        {
            "user_pub_key": "9d54e1076976a0a287de0dc1c51ae3a23d876556d0dab99",
            "timestamp": 1585412837, 
            "latitude": 24.953606,
            "longitute": 121.4095702,
            "stay_home": 1,
            "image_cid": "QmTddVonVQszEX141sTLpc3sj2uzujDrtp6JXzTjKz8tGf",
            "body_temperature": 36.5,
            "coughing": 0,
            "running_nose": 1,
            "equipment": "forehead"
        },
        {
            "user_pub_key": "9d54e1076976a0a287de0dc1c51ae3a23d876556d0dab99",
            "timestamp": 1585391249, 
            "latitude": 24.953606,
            "longitute": 121.4095702,
            "stay_home": 1,
            "image_cid": "QmWLsWkcpeYBFJtvzGrdp9KH8LjZM4z5oATDqRAu13hNnF",
            "body_temperature": 37.3,
            "coughing": 1,
            "running_nose": 1,
            "equipment": "forehead"
        },
        {
            "user_pub_key": "9d54e1076976a0a287de0dc1c51ae3a23d876556d0dab99",
            "timestamp":  	1585362464, 
            "latitude": 24.969977,
            "longitute": 121.4013523,
            "stay_home": 0,
            "image_cid": "",
            "body_temperature": 37.3,
            "coughing": 1,
            "running_nose": 1,
            "equipment": "forehead"
        },
        {
            "user_pub_key": "9d54e1076976a0a287de0dc1c51ae3a23d876556d0dab99",
            "timestamp":  1585408843, 
            "latitude": 24.953606,
            "longitute": 121.4095702,
            "stay_home": 0,
            "image_cid": "",
            "body_temperature": 37.0,
            "coughing": 0,
            "running_nose": 0,
            "equipment": "forehead"
        }
    ]   
    return monitoring_data



# Create your views here.
def home(request):
    data = get_data()
    updated_data = data
    context = {
        'measurement': updated_data,
        'timestamps': [datetime.fromtimestamp(d['timestamp']).date() for d in data]
        
    }
    return render(request, 'dashboard/dashboard.html', context)


def population_chart(request):
    data =  get_data()
    
    timestamps = [d['timestamp'] for d in data]
    measurements_fever = [d['body_temperature'] for d in data]

    first_day = min(timestamps)
    labels = timestamps

    measurements_max = [31,31,33]
    measurements_min =[3,3,4]
    critical_line = [37.5, 37.5, 37.5]

    return JsonResponse(data={
        'labels': labels,
        'measure_fever_max': measurements_max,
        'measure_fever_min': measurements_min,
        'threshold': critical_line
    })