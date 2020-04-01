import requests
import pandas as pd
from datetime import datetime

import logging

MIN_BODY_TEMP = 35
MAX_BODY_TEMP = 43

logger = logging.getLogger('models')

def request_json_data(url):
    response =  requests.get(url).json()
    response = response
    return response

#Load Data from CID
def load_CID_data():
    #THE MAIN IPFS URL
    main_url = 'https://gateway.pinata.cloud/ipfs/'
    
    #NEED TO FIND A SMART WAY TO SHARE THE HASHES SO THAT THE DATA CAN BE DOWNLOADED FROM IPFS
    hashes = ['QmT1secRZXYoB1ToyhJHyzhqCh5iJzopjhBgidyMDdvRFC', 'QmQuK3UyHsCbXVmdsbYRzeozJNhCfTB6uM6NmxUygMQJsx','QmboKqvmxd5qbqRRLaRwPERu8gyZBe75WhoV6NAZcyirK9','QmNZKVfVMFrQJJ2DiR23oNw8h5z7jeUP2SzkcRW1Ja67S8']
    data = []

    #LOOP THROUGH ALL HASHES AND BUILD THE JSON
    for hash in hashes:
        url = main_url + hash
        print(url)
        data.append(request_json_data(url))
        
    return data

# Add Validation Functions
def validation_fever(measurement):
        try:
            float(measurement) >= MIN_BODY_TEMP
            float(measurement <= MAX_BODY_TEMP)
    
        except ValueError:
            logger.error(f'Body Temperature outside of normal range: {measurement}')
        else:
            return measurement


# Time Validation
def validation_time(time_submitted):
    if(time_submitted != 0 and time_submitted <= datetime.now ):
        #STORE INTO DB
        pass
    else:
        logger.error(f'Timestamp greater than current time, {time_submitted}')

# Location Check, make sure the location is not 0, 0
def validatation_location(latitude, longitude):
    if(latitude != 0 and longitude != 0):
        # Store to DB
        logger(f'lat: {latitude}, long: {longitude}')
    elif latitude == 0 and longitude != 0:
        # Strote to DB
        logger(f'lat: {latitude}, long: {longitude}')
    elif latitude != 0 and longitude == 0:
        pass
    
    