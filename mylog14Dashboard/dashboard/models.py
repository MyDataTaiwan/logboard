import requests
import pandas as pd

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