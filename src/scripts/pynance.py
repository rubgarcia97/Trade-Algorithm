from urllib.parse import urlencode
from datetime import datetime

import json
import requests
import hmac
import urllib
import hashlib
import time
import pandas as pd
import math

class Client:

    '''
    Define todas las funciones necesarias para poder generar las credenciales de seguridad
    '''

    def __init__(self):


        '''Extraccion de las credenciales en base a la ruta proporcionada desde el constructor'''
        self.__path = "../../api_binance.json"
        self.URL = "https://api.binance.com"

        if self.__path is not None:
            with open(self.__path, 'r') as file:
                data = json.load(file)
                self.__apiKey = data.get('apiKey', None)
                self.__secretKey = data.get('secretKey', None)
        else:
            self.__apiKey = None
            self.__secretKey = None
        


    def signature(self,query_string):

        return hmac.new(
            self.__secretKey.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()
    

    def get_timestamp(self):
        return int(time.time() * 1000)
    

    def base_request(self, http_method, signed: bool, endpoint:str, params=None):

        endpoint = endpoint
        if params is None:
            load_params = {}
        else:
            load_params = params

        if signed:
            query_string = urlencode(load_params,True)
            if query_string:
                query_string = f"{query_string}&timestamp={self.get_timestamp()}"
            else:
                query_string = "timestamp={}".format(self.get_timestamp())
            
            url = (
                self.URL + endpoint + "?" + query_string + "&signature=" + Client().signature(query_string)
            )
            print(f"{http_method} {url}")
            params = {
                "url": url,
                #"params": load_params
            }

            session = requests.Session()
            session.headers.update(
                {"Content-Type" : "application/json;charset=utf-8", "X-MBX-APIKEY": self.__apiKey}
            )

            return {
                "GET" : session.get,
                "DELETE" : session.delete,
                "PUT" : session.put,
                "POST" : session.post,
            }.get(http_method, "GET")(**params).json()

        else:
            url = (
                self.URL + endpoint
            )
            params = {
                "url" : url,
                "params" : params
            }

            session = requests.Session()
            return {
                "GET" : session.get,
                "DELETE" : session.delete,
                "PUT" : session.put,
                "POST" : session.post,
            }.get(http_method, "GET")(**params).json()



class Pynance:
    
    '''
    Define todas las interacciones entre la API de Binance y nosotros
    '''

    
    def __init__(self):

        self.URL = "https://api.binance.com"

        # Acceso a los datos generados por signature.Client
        self.client = Client()


    def exchange_information (self,
                              symbol:str)->json:
        
        response = Client().base_request(http_method="GET",signed=False,endpoint="/api/v3/exchangeInfo",params={"symbol":symbol})

        with open("../results/info_"+symbol+".json", 'w') as file:
            file.write(json.dumps(response, indent=4))

        print(response)
        
    

    def wallet(self,save:bool):

        response = Client().base_request(http_method="GET",signed=True,endpoint="/api/v3/account")
        response = {'balances' : [balance for balance in response['balances'] if float(balance['free']) != 0]}


        if save:
            with open("../results/wallet.json", 'w') as file:
                file.write(json.dumps(response, indent=4))
        else:
            return response


    def market_data(self, symbol:str,interval:int,save:bool, lags=None):

        dict = {symbol:[]}
        for lag in range(lags):

            begin = time.time()

            response = Client().base_request(http_method="GET",signed=False,endpoint="/api/v3/ticker/price",params={"symbol":symbol})
            timestamp = datetime.utcfromtimestamp(Client().get_timestamp()/1000).strftime('%Y-%m-%d %H:%M:%S')
            price = response["price"]

            dict[symbol].append({"timestamp":timestamp,"price": price})

            end = time.time()
            
            try:
                time.sleep(interval-end+begin)
            except: 
                continue
            
            
        if save:
            with open("../results/"+symbol+"_price.json", 'w') as file:
                file.write(json.dumps(dict, indent=4))
        else:
            return dict
    

    def candlestick_data(self,
                        symbol:str,
                        intervals:str,
                        limit:int = None) -> json:  

        data = {symbol:[]}
        keys = ["openTime","OpenPrice","HighPrice","LowPrice","ClosePrice","Volume","closeTime","QuoteAssetVolume","nTrades"]
        response = Client().base_request(http_method="GET",signed=False,endpoint="/api/v3/uiKlines",params={"symbol":symbol,"interval":intervals,"limit":limit})
        
        for row in response:
            dict = {}
            for i,key in enumerate(keys):
                if key in ("openTime","closeTime"):
                    dict[key] = datetime.utcfromtimestamp(int(row[i])/1000).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    dict[key] = row[i]
            data[symbol].append(dict)

        
        with open("../results/"+symbol+"_candlestick.json", 'w') as file:
            file.write(json.dumps(data, indent=4))


    def spot_order(self,
                   params:dict) -> json: 
        
        
        response = Client().base_request(http_method="POST",signed=True,endpoint="/api/v3/order/test",params=params)

        return response
        '''
        with open("../results/firstsell.json", 'w') as file:
            file.write(json.dumps(response, indent=4))
        '''

        
        

if __name__=="__main__":

    params = {
        "symbol":"BTCUSDT",
        "side":"SELL",
        "type":"MARKET",
        "quantity":5
    }
    
    response = Pynance().spot_order(params=params)
    print(response)


    
    