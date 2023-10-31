from binance import Pynance

import pandas as pd
import numpy as np
import json


def strategy_1():

    """
    En esta primera estrategia, definiremos signals de compra y de venta.

    El criterio a seguir sera el de: P > MA[n] para buy signals y P<MA[n] para sell signals
    """

    Pynance().market_data(symbol="BTCUSDT",lags=300,interval=1)

    with open("../results/BTCUSDT_price.json",'r') as f:
        data = json.loads(f.read())
    data = pd.json_normalize(data,record_path=['BTCUSDT'])
    data = data.set_index('timestamp')

    data["MA_5"] = data.price.rolling(5).mean()
    data["MA_25"] = data.price.rolling(25).mean()
    data["MA_50"] = data.price.rolling(50).mean()
    
    data["signal"] = np.where(
        (data['price'].notna()) & (data['MA_25'].notna()),
        np.where(data['price'] > data['MA_25'], 'buy', 'sell'),
        np.nan  # En caso de NaN, establece 'signal' como NaN
    )


    print(data)




if __name__=="__main__":
    strategy_1()