from binance import Pynance

import pandas as pd
import numpy as np
import json


def strategy_1(wallet):

    """
    En esta primera estrategia, definiremos signals de compra y de venta.

    El criterio a seguir sera el de: P > MA[n] para buy signals y P<MA[n] para sell signals

    
    """

    Pynance().market_data(symbol="BTCUSDT",lags=1200,interval=1)

    with open("../results/BTCUSDT_price.json",'r') as f:
        data = json.loads(f.read())
    data = pd.json_normalize(data,record_path=['BTCUSDT'])
    data = data.set_index('timestamp')

    #Transform variables
    data["price"] = data["price"].astype(float)


    #Add columns
    data["MA_5"] = data.price.rolling(5).mean()
    data["MA_25"] = data.price.rolling(25).mean()
    data["MA_50"] = data.price.rolling(50).mean()
    
    data["signal"] = np.where(
        (data['price'].notna()) & (data['MA_25'].notna()),
        np.where(data['price'] > data['MA_25'], 'buy', 'sell'),
        np.nan  # En caso de NaN, establece 'signal' como NaN
    )

    #Save dataframe
    data.to_csv("../results/strategy_1/strategy_1_raw.csv", index=True)


    # ============================== STRATEGY ==============================

    results = []

    wallet = wallet
    prev_signal = None

    try:

        for row in range(len(data)):
            
            if data.iloc[row, 4] == "buy" and prev_signal != "buy":
                wallet = np.divide(wallet,data.iloc[row,0])
                prev_signal = data.iloc[row, 4]

                results.append({"index": data.index[row], "wallet": wallet * data.iloc[row,0]})

            elif data.iloc[row, 4] == "sell" and prev_signal not in ["sell",None]:
                wallet = np.multiply(wallet,data.iloc[row,0])
                prev_signal = data.iloc[row, 4]

                results.append({"index": data.index[row], "wallet": wallet})

            else:
                continue

        df = pd.DataFrame(results)
        df['index'] = pd.to_datetime(df['index'])
        df.set_index('index', inplace=True)

    except KeyError:
        print("No se ha dado ninguna 'buy signal'")
    
    #calculate profitability
    
    t0 = df.iloc[0,0]
    t1 = df.iloc[-1,0]

    rentabilidad = (t1 - t0)/t0
    print(format(rentabilidad, ".2%"))

    #save results

    with open("../results/strategy_1/strategy_1_results.csv", 'w') as csv_file:
        df.to_csv(csv_file, index=False, header=True)





if __name__=="__main__":
    strategy_1(wallet=100)