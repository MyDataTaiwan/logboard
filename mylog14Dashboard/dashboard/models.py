from django.utils import timezone
from django.db import models
from django.urls import reverse

import requests
import pandas as pd
from datetime import datetime

import logging

# Temperature Constants for verification and line threshhold
MIN_BODY_TEMP = 35
MAX_BODY_TEMP = 43
CRITICAL_TEMP  = 37.5

logger = logging.getLogger('models')

# TODO 001 Aggregate the timestamps specific day get the max temp. and min. temp
# TODO Change default values to something more useful    
# TODO Write the class to store the authorised hashes from the user to generate the unique dashboard

class Measurement(models.Model):
    title = 'dashboard'
    CELSIUS = 'C'
    FARENHEIT = 'F'

    TEMPERATURE_UNIT_CHOICES = [
        (CELSIUS, 'C'),
        (FARENHEIT, 'F')
    ]

    userHash = models.SlugField(max_length=100, default='test_hash')
    bodyTemperature = models.FloatField(default=36.5)
    bodyTemperatureUnit = models.CharField(
        max_length=1,
        choices=TEMPERATURE_UNIT_CHOICES,
        default=CELSIUS,
    )
    coughing = models.IntegerField(default=0)
    headache = models.IntegerField(default=0)
    runnyNose = models.IntegerField(default=0)
    soreThroat = models.IntegerField(default=0)
    tasteLoss = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default="")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)

class AuthCustodianHashes(models.Model):
    userHash = models.SlugField(max_length=100, default='test_hash')
    reviewStatus = models.IntegerField(default=0)

"""
main_url = 'https://gateway.pinata.cloud/ipfs/'
hashes = ['QmT1secRZXYoB1ToyhJHyzhqCh5iJzopjhBgidyMDdvRFC', 'QmQuK3UyHsCbXVmdsbYRzeozJNhCfTB6uM6NmxUygMQJsx','QmboKqvmxd5qbqRRLaRwPERu8gyZBe75WhoV6NAZcyirK9','QmNZKVfVMFrQJJ2DiR23oNw8h5z7jeUP2SzkcRW1Ja67S8']

for hash in hashes:
    url = main_url + hash
    response =  requests.get(url).json()
    monitoring_data.append(response)

# Create a Django model object for each object in the JSON 
for id in monitoring_data['user_pub_key']:
    Measurement.objects.create(id=monitoring_data['user_pub_key'], name=monitoring_data['timestamp'])
"""