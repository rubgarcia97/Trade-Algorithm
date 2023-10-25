from urllib.parse import urlencode

import json
import requests
import hmac
import urllib
import hashlib
import time

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
    

    def dispatch_request(self, http_method):

        session = requests.Session()
        session.headers.update(
            {"Content-Type" : "application/json;charset=utf-8", "X-MBX-APIKEY": self.__apiKey}
        )

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
        
        url = (self.URL + url_path + "?" + query_string + "&signature=" + Client().signature(query_string)

        )
        
        print(f"{http_method} {url}")
        params = {
            "url": url,
            "params": {}
        }
        response = Client().dispatch_request(http_method)(**params)
        response = response.json()
        #response = [balance for balance in response['balances'] if float(balance['free']) != 0]

        #response = {'balances' : response}

        with open("./test.json", 'w') as file:
            file.write(json.dumps(response, indent=4))
        

if __name__=="__main__":
    
    Pynance().wallet(http_method="GET", url_path='/api/v3/account')