from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.conf import settings

from datetime import datetime
from PIL import Image

# some hashing imports that could be usefull
#import hashlib
#import zlib
#import urllib

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

    user_token = models.IntegerField(default=0)
    userHash = models.SlugField(max_length=100, default='abcdefg')
    bodyTemperature = models.FloatField(default=36.5)
    bodyTemperatureUnit = models.CharField(
        max_length=1,
        choices=TEMPERATURE_UNIT_CHOICES,
        default=CELSIUS,
    )
    bodyTemperatureMAX = models.FloatField(default=MAX_BODY_TEMP)
    bodyTemperatureMIN = models.FloatField(default=MIN_BODY_TEMP)
    bodyTemperatureCRITICAL = models.FloatField(default=CRITICAL_TEMP)
    timestamp = models.DateTimeField(default=timezone.now)
    image_id = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('dashboard-details', kwargs={'slug': self.userHash})

class AuthCustodianHashes(models.Model):
    userHash = models.SlugField(max_length=100, default='test_hash')
    reviewStatus = models.IntegerField(default=0)
    lastChange = models.DateTimeField(default=timezone.now)

class Snapshot(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)

class Condition(models.Model):
    timestamp = models.ForeignKey("Measurement", on_delete=models.CASCADE)
    coughing = models.IntegerField(default=0)
    headache = models.IntegerField(default=0)
    runnyNose = models.IntegerField(default=0)
    soreThroat = models.IntegerField(default=0)
    tasteLoss = models.IntegerField(default=0)

class Photos(models.Model):
    photo_id = models.IntegerField(default=0)
    file_path = models.ImageField(default='/media/custodian_pics/mylog14-03_YSaAO0C.png', upload_to='media/custodian_pics')

"""
class UniqueURL(models.Model):
    
    url = models.CharField(max_length=100)
    measure = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    expiration_date = models.DateField()
    ref_object = models.ForeignKey(class_to_import, on_delete=models.CASCADE)
    url_hash = models.CharField(max_length=200)
    clics = models.IntegerField()


    def encode_url(self):
        test = "hash_test"
        data =  [test]

        my_url = zlib.compress(pickle.dumps(data, 0)).encode('base64').replace('\n', '')
        my_hash = hashlib.sha256(settings.UNIQUE_HASH_CODE + my_url).hexdigest()[:12]
        self.url = my_url
        self.url_hash = my_hash
        self.save()
        return my_hash, my_url

    def decode_url(self, my_hash, my_url):
        my_url = urllib.unquote(url)
        m =  hashlib.sha256(settings.UNIQUE_HASH_CODE + my_url).hexdigest()[:12]
        if m != my_hash:
            raise Exception("Wrong Hash please try again!")
        data = pickle.loads(zlib.decompress(my_url.decode('base')))
        return data
"""