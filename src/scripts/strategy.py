from binance import Pynance
from gui import GUI
from datetime import datetime
from tkinter import *

import pandas as pd
import numpy as np
import json
import time
import customtkinter
import threading

now = datetime.now().strftime("%d-%m-%Y_%H%M%S")
stop = None

def strategy_1beta(symbol:str, interval:int, SMA_periods:int, save:bool):


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

    global stop

    #wallet = wallet
    prev_signal = None

    MA = f"MA_{SMA_periods}"

    data = pd.DataFrame(columns=['price',MA,"signal"])
    results = pd.DataFrame(columns=['amount'])

    while stop is None:
    
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
            response = Pynance().spot_order(params={"symbol":"BTCUSDT","side":"BUY","type":"MARKET","quoteOrderQty":5})
            #wallet = np.divide(wallet,data.loc[timestamp,"price"])
            if len(response)>2:
                prev_signal = data.loc[timestamp,'signal']               

            else:
                continue


        elif data.loc[timestamp,'signal'] == "sell" and prev_signal not in ["sell",None]:
                response = Pynance().spot_order(params={"symbol":"BTCUSDT","side":"SELL","type":"MARKET","quoteOrderQty":5})

                if len(response)>2:
                    prev_signal = data.loc[timestamp,'signal']

                    transact_time = response['transactTime']
                    transact_time = datetime.utcfromtimestamp(transact_time/1000).strftime('%Y-%m-%d %H:%M:%S')
                    amount = Pynance().wallet(save=False)
                    amount = float(amount['balances'][0]['free'])

                    results.loc[transact_time] = amount

                else:
                    continue

        else:
            continue
    
    else:
        pass

    #calculate profitability
    t0 = results.iloc[0,0]
    t1 = results.iloc[-1,0]

    rentabilidad = (t1 - t0)/t0
    print(format(rentabilidad, ".2%"))
        

    if save:
        data.to_csv("../results/strategy_1/strategy_1beta_raw_"+str(now)+".csv", index=True)
        results.to_csv("../results/strategy_1/strategy_1beta_results_"+str(now)+".csv", index=True)
    else:
        pass


def cerrar_ventana():
    global stop
    stop = "exit"

    print(f"Repliegue de las tropas a las: {datetime.now()}")
    GUI.root.quit()
    

def iniciar_estrategia():
    global stop
    stop = None
    print(f"El general Trajano ha desplegado sus legiones a las: {datetime.now()}")
    threading.Thread(target=strategy_1beta, args=("BTCUSDT", 1, 25, True)).start()


if __name__=="__main__":

    GUI().gui(inicio=iniciar_estrategia,detener=cerrar_ventana)


