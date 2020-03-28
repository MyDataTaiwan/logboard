from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
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

def home(request):
    context = {
        'measurement': monitoring_data
    }
    return render(request, 'dashboard/dashboard.html', context)


def population_chart(request):
    labels = []
    measurements_fever = []



    measurements_max = [40.1,38.5,38.1]
    measurements_min = [35.8,36.5,38.1]

    return JsonResponse(data={
        'labels': labels,
        'measure_fever': measurements_fever,
        'measure_fever_min': measurements_min,
        'measure_fever_max': measurements_max
    })

def test(request):
    return render(request, 'dashboard/test.html')