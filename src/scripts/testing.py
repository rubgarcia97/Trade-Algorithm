from binance.spot import Spot
from urllib.parse import urlencode


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




def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type":"application/json;charset=utf-8", "X-MBX-APIKEY":apiKey}
    )
    return {
        "GET" : session.get,
        "DELETE" : session.delete,
        "PUT" : session.put,
        "POST" : session.post,
    }.get(http_method, "GET")




# ================== Request ==================


def signed_request(http_method,url_path,load_params={}):

    query_string = urlencode(load_params,True)

    if query_string:
        query_string = f'{query_string}&timestamp={get_timestamp()}'
    else:
        query_string = f'timestamp={get_timestamp()}'

    url = (
        "https://api.binance.com" + url_path + "?" + query_string + "&signature=" + signature(query_string)
    )

    print(f"{http_method} {url}")
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    
    return response.json()
    


'''
url = "https://api.binance.com/api/v3/"
endpoint = "ticker/price"

params = {
    'symbol': "ETHUSDT"
}


request = requests.get(url=url+endpoint, params=params)
response = request.json()



with open('./test.json','w') as file:
    file.write(json.dumps(response))
'''  
# https://github.com/binance/binance-signature-examples/blob/master/python/spot/spot.py
# https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
# https://python.plainenglish.io/automate-your-crypto-trading-with-python-a-step-by-step-guide-to-building-a-binance-trading-bot-a658f565f0b2
# https://github.com/binance/binance-signature-examples/blob/master/python/hmac_sha256_signature.py

if __name__=='__main__':

    
    with open("../../api_binance.json",'r') as file:
        data = json.load(file)
        apiKey = data.get('apiKey',None)
        secretKey = data.get('secretKey',None)

    response = signed_request(http_method="GET", url_path='/api/v3/account')
    response = [balance for balance in response['balances'] if float(balance['free']) != 0]

    response = {'balances':response}

    with open('./test.json','w') as file:
        file.write(json.dumps(response, indent=4))
