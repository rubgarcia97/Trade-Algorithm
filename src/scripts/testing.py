from binance.spot import Spot

import sys
import os
import time
import json
import requests
import hmac
import hashlib

# ================== Api token ==================


with open("../../api_binance.json",'r') as file:
    data = json.load(file)
    apiKey = data.get('apiKey',None)
    secretKey = data.get('secretKey',None)



def signature(query_string):
    return hmac.new(
        secretKey.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    return int(time.time() * 1000)
    

# ================== Request ==================

url = "https://api.binance.com/api/v3/"
endpoint = "ticker/price"

params = {
    'symbol': "ETHUSDT"
}


request = requests.get(url=url+endpoint, params=params)
response = request.json()



with open('./test.json','w') as file:
    file.write(json.dumps(response))
    
# https://github.com/binance/binance-signature-examples/blob/master/python/spot/spot.py
# https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
# https://github.com/binance/binance-signature-examples/blob/master/python/hmac_sha256_signature.py