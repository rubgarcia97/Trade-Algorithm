from pynance import Pynance
from datetime import datetime
from tkinter import *

import pandas as pd
import numpy as np
import json
import time
import customtkinter
import threading
import math


class Strategies:

    def __init__(self):
        
        self.__now = datetime.now().strftime("%d-%m-%Y_%H%M%S")
        self.__stop = None
        self.__wallet = 8

    def strategy_1beta(self,symbol:str, interval:int, SMA_periods:int, save:bool):

        """
        En esta primera estrategia, definiremos signals de compra y de venta.

        El criterio a seguir sera el de: P > MA[n] para buy signals y P<MA[n] para sell signals

        :param symbol:required
        :param interval: segundos que dejaremos pasar entre iteracion
        :param SMA_periods: n periodos de calculo del SMA
        :param save: Guardar los resultados en .csv
        """

        MA = f"MA_{SMA_periods}"

        data = pd.DataFrame(columns=['price',MA,"signal"]) #Dataframe donde se ejecuta la estrategia

        #while self.__stop is None:
        for i in range(27):
        
            #Obtenemos información del precio y construimos nuestro DF de evaluación de signals
            result = Pynance().market_data(symbol=symbol,lags=1,interval=interval,save=False)

            timestamp = result["timestamp"]
            price = float(result["price"])

            data.loc[timestamp] = price
            data[MA] = data.price.rolling(SMA_periods).mean()
            data["signal"] = np.where(
                (data['price'].notna()) & (data[MA].notna()),
                np.where(data['price'] > data[MA], 'buy', 'sell'),
                np.nan  # En caso de NaN, establece 'signal' como NaN
            )
        
        print(data)


    
    def cross_RSI_7(self):
        time.sleep(10)
        print("Hello world")



if __name__ == "__main__":

    Strategies().strategy_1beta(symbol="BTCUSDT",interval=2,SMA_periods=10,save=False)