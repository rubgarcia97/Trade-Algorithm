from scripts.pynance import Pynance
from scripts.gui import GUI
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

    def strategy_1beta(self,symbol:str, interval:int, SMA_periods:int, save:bool):

        

        """
        En esta primera estrategia, definiremos signals de compra y de venta.

        El criterio a seguir sera el de: P > MA[n] para buy signals y P<MA[n] para sell signals

        :param symbol:required
        :param wallet: Importe inicial de la cartera que se utilizara para la primera operacion
        :param lags: iteraciones del bucle
        :param interval: segundos que dejaremos pasar entre iteracion
        :param SMA_periods: n periodos de calculo del SMA
        :param save: Guardar los resultados en .csv
        """

        global wallet

        wallet = 8
        prev_signal = None

        MA = f"MA_{SMA_periods}"

        data = pd.DataFrame(columns=['price',MA,"signal"])
        results = pd.DataFrame(columns=['timestamp','signal','price','qty','total','fee','wallet']).set_index('timestamp')

        while self.__stop is None:
        
            result = Pynance().market_data(symbol=symbol,lags=1,interval=interval,save=False)

            symbol_data = result[symbol][0]
            price = float(symbol_data["price"])
            timestamp = pd.to_datetime(symbol_data["timestamp"])

            data.loc[timestamp] = price

            
            data[MA] = data.price.rolling(SMA_periods).mean()
            data["signal"] = np.where(
                (data['price'].notna()) & (data[MA].notna()),
                np.where(data['price'] > data[MA], 'buy', 'sell'),
                np.nan  # En caso de NaN, establece 'signal' como NaN
            )

            if data.loc[timestamp,'signal'] == "buy" and prev_signal != "buy":

                price = data.loc[timestamp,"price"]
                prev_signal = data.loc[timestamp,"signal"]
                
                qty_buy = math.floor(wallet/(price*0.00001))*0.00001
                total_buy = price * qty_buy
                fee_buy = total_buy*0.00100

                wallet = qty_buy-(qty_buy*0.00100)

                dict={
                    'signal' : data.loc[timestamp,'signal'],
                    'price' : price,
                    'qty' : qty_buy,
                    'total': total_buy,
                    'fee' : fee_buy,
                    'wallet' : wallet
                }
                results.loc[timestamp] = dict
                print(dict)


                '''Funcional
                response = Pynance().spot_order(params={"symbol":"BTCUSDT","side":"BUY","type":"MARKET","quoteOrderQty":8})
                #wallet = np.divide(wallet,data.loc[timestamp,"price"])
                if len(response)>2:
                    prev_signal = data.loc[timestamp,'signal']               

                else:
                    continue
                '''


            elif data.loc[timestamp,'signal'] == "sell" and prev_signal not in ["sell",None]:
                    
                    price = data.loc[timestamp,"price"]
                    prev_signal = data.loc[timestamp,"signal"]
                    
                    qty_sell = round(wallet,5)
                    total_sell = price * qty_sell
                    fee_sell = total_sell*0.00100

                    wallet = total_sell - fee_sell

                    dict={
                        'signal' : data.loc[timestamp,'signal'],
                        'price' : price,
                        'qty' : qty_sell,
                        'total': total_sell,
                        'fee' : fee_sell,
                        'wallet' : wallet
                    }
                    results.loc[timestamp]=dict
                    print(dict)


                    '''Funcional
                    wallet = Pynance().wallet(save=False)
                    wallet_df = pd.DataFrame(wallet["balances"])
                    free = wallet_df[wallet_df["asset"] == "BTC"]["free"].values[0]
                    free = math.floor(float(free)*10000)/10000

                    response = Pynance().spot_order(params={"symbol":"BTCUSDT","side":"SELL","type":"MARKET","quantity":free})

                    if len(response)>2:
                        prev_signal = data.loc[timestamp,'signal']

                        transact_time = response['transactTime']
                        transact_time = datetime.utcfromtimestamp(transact_time/1000).strftime('%Y-%m-%d %H:%M:%S')
                        amount = Pynance().wallet(save=False)
                        amount = float(amount['balances'][0]['free'])

                        results.loc[transact_time] = amount

                    else:
                        continue
                    '''

            else:
                continue
        
        else:
            pass

        #calculate profitability
        t0 = results["total"].iloc[0]
        t1 = results["total"].iloc[-1]

        rentabilidad = (t1 - t0)/t0
        print(format(rentabilidad, ".2%"))
            

        if save:
            data.to_csv("../results/strategy_1/strategy_1beta_raw_"+str(self.__now)+".csv", index=True)
            results.to_csv("../results/strategy_1/strategy_1beta_results_"+str(self.__now)+".csv", index=True)
        else:
            pass
    
    def cross_RSI_7(self):
        time.sleep(10)
        print("Hello world")


