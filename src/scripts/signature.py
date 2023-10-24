import json
import hmac
import hashlib
import time
import requests


class Client:

    '''
    Define todas las funciones necesarias para poder generar las credenciales de seguridad
    '''

    def __init__(self,json_path):

        '''Extraccion de las credenciales en base a la ruta proporcionada desde el constructor'''
        
        with open(json_path, 'r') as file:
            data = json.load(file)
            self.__apiKey = data.get('apiKey', None)
            self.__secretKey = data.get('secretKey', None)


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



if __name__ == '__main__':

    Client("../../api_binance.json").signature()