from binance import Pynance
from datetime import datetime

import pandas as pd
import numpy as np
import json
import time


def strategy_1(symbol:str,wallet:int, lags:int, interval:int, SMA_periods:int, save:bool):


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

    wallet = wallet
    prev_signal = None

    MA = f"MA_{SMA_periods}"

    data = pd.DataFrame(columns=['price',MA,"signal"])
    results = pd.DataFrame(columns=['wallet'])

    for lag in range(lags):
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
            wallet = np.divide(wallet,data.loc[timestamp,"price"])
            prev_signal = data.loc[timestamp,'signal']

            results.loc[timestamp] = wallet * data.loc[timestamp,"price"]


        elif data.loc[timestamp,'signal'] == "sell" and prev_signal not in ["sell",None]:
            wallet = np.multiply(wallet,data.loc[timestamp,"price"])
            prev_signal = data.loc[timestamp,'signal']

            results.loc[timestamp] = wallet

        else:
            continue

    #calculate profitability
    t0 = results.iloc[0,0]
    t1 = results.iloc[-1,0]

    rentabilidad = (t1 - t0)/t0
    print(format(rentabilidad, ".2%"))
        

    if save:
        data.to_csv("../results/strategy_1/strategy_1_raw.csv", index=True)
        results.to_csv("../results/strategy_1/strategy_1_results.csv", index=True)
    else:
        pass




if __name__=="__main__":

    strategy_1(symbol="BTCUSDT",wallet=100,lags=900,interval=1,SMA_periods=25,save=True)