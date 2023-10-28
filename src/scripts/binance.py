from urllib.parse import urlencode

import json
import requests
import hmac
import urllib
import hashlib
import time
import datetime

class Client:

    '''
    Define todas las funciones necesarias para poder generar las credenciales de seguridad
    '''

    def __init__(self):


        '''Extraccion de las credenciales en base a la ruta proporcionada desde el constructor'''
        self.__path = "../../api_binance.json"

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
    

    def base_request(self, http_method, signed: bool):

        session = requests.Session()

        if signed:
            session.headers.update(
                {"Content-Type" : "application/json;charset=utf-8", "X-MBX-APIKEY": self.__apiKey}
            )

            return {
                "GET" : session.get,
                "DELETE" : session.delete,
                "PUT" : session.put,
                "POST" : session.post,
            }.get(http_method, "GET")
        
        else:
            return {
                "GET" : session.get,
                "DELETE" : session.delete,
                "PUT" : session.put,
                "POST" : session.post,
            }.get(http_method, "GET")



class Pynance:
    
    '''
    Define todas las interacciones entre la API de Binance y nosotros
    '''

    
    def __init__(self):

        self.URL = "https://api.binance.com"

        # Acceso a los datos generados por signature.Client
        self.client = Client()
        
    

    def wallet(self,http_method,url_path,load_params={}):

        query_string = urlencode(load_params,True)
        if query_string:
            query_string = f"{query_string}&timestamp={self.client.get_timestamp()}"
        else:
            query_string = "timestamp={}".format(self.client.get_timestamp())
        
        url = (
            self.URL + url_path + "?" + query_string + "&signature=" + Client().signature(query_string)
        )
        
        print(f"{http_method} {url}")
        params = {
            "url": url,
            "params": {}
        }
        response = Client().base_request(http_method,signed=True)(**params).json()
        response = {'balances' : [balance for balance in response['balances'] if float(balance['free']) != 0]}


        with open("../results/wallet.json", 'w') as file:
            file.write(json.dumps(response, indent=4))


    def market_data(self, symbol:str, periods=None):
        
        endpoint = "/api/v3/ticker/price"

        url = (
            self.URL + endpoint 
        )
        params = {
            "url" : url,
            "params" : {
                "symbol" : symbol
            }
        }

        dict = {symbol:[]}
        for lag in range(periods):

            begin = time.time()

            response = Client().base_request("GET",signed=False)(**params).json()
            price = response["price"]
            timestamp = Client().get_timestamp()

            dict[symbol].append({"price": price, "timestamp":timestamp})

            end = time.time()
            print(end - begin)
            



        with open("../results/"+symbol+"_price.json", 'w') as file:
            file.write(json.dumps(dict, indent=4))
    

    def candlestick_data(
            self,
            symbol:str,
            intervals:str,
            **kwargs
    ):
        endpoint = "/api/v3/klines"
        url = (
            self.URL + endpoint
        )
        params = {
            "url": url,
            "params": {
                "symbol": symbol,
                "interval": intervals 
            }
        }
        
        data = {symbol:[]}
        keys = ["openTime","OpenPrice","HighPrice","LowPrice","ClosePrice","Volume","CloseTime","QuoteAssetVolume","nTrades"]
        response = Client().base_request("GET",signed=False)(**params).json()
        
        for row in response:
            dict = {}
            for i,key in enumerate(keys):
                dict[key] = row[i]
            data[symbol].append(dict)

        
        with open("../results/"+symbol+"_candlestick.json", 'w') as file:
            file.write(json.dumps(data, indent=4))
        
        

if __name__=="__main__":
    
    Pynance().candlestick_data(symbol="ETHUSDT",intervals="1s")