from django.utils import timezone
from django.db import models
from django.urls import reverse

import requests
import pandas as pd
from datetime import datetime
from PIL import Image

import logging

# Temperature Constants for verification and line threshhold
MIN_BODY_TEMP = 35
MAX_BODY_TEMP = 42
CRITICAL_TEMP  = 37.5

logger = logging.getLogger('models')

# TODO 001 Aggregate the timestamps specific day get the max temp. and min. temp
# TODO Body Temperature needs to be converted if Farenheit, or Celcius
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
    bodyTemperatureMAX = models.FloatField(default=MAX_BODY_TEMP)
    bodyTemperatureMIN = models.FloatField(default=MIN_BODY_TEMP)
    bodyTemperatureCRITICAL = models.FloatField(default=CRITICAL_TEMP)
    coughing = models.IntegerField(default=0)
    headache = models.IntegerField(default=0)
    runnyNose = models.IntegerField(default=0)
    soreThroat = models.IntegerField(default=0)
    tasteLoss = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='/media/custodian_pics/mylog14-03_YSaAO0C.png', upload_to='media/custodian_pics')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    
    def get_absolute_url(self):
        return reverse('dashboard-detail', kwargs={'slug': self.userHash})

class AuthCustodianHashes(models.Model):
    userHash = models.SlugField(max_length=100, default='test_hash')
    reviewStatus = models.IntegerField(default=0)
    lastChange = models.DateTimeField(default=timezone.now)