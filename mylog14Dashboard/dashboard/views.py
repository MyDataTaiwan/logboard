from django.shortcuts import render
# Create your views here.

signature_data = [
    {
        'data': 'Qmaaaaaaaa',
        'metadata': 'Qmbbbbbbbbb',
        'signature_data': 'Qmcccccccc',
        'signature_metadata':'Qmdddddddd'
    }

]

monitoring_data = [
    {
        'date': '2020-03-27',
        'body_temp_max': '37.2',
        'body_temp_min': '36.7',
        'coughing': 'no',
        'running_nose': 'no'
    },
    {
        'date': '2020-03-28',
        'body_temp_max': '38.4',
        'body_temp_min': '37.2',
        'coughing': 'no',
        'running_nose': 'no'
    }
]

def home(request):
    context = {
        'measurement': monitoring_data
    }
    return render(request, 'dashboard/home.html', context)