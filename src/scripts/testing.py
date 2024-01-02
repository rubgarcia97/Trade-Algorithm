import pandas as pd
import numpy as np
import math

from strategy import Strategies
from pynance import Pynance

class Testing(Strategies):

    def __init__(self):
        super().__init__()
    

    def cross_SMA(self,symbol:str, interval:int, SMA_periods:int, save:bool):
        

        """
        En esta primera estrategia, definiremos signals de compra y de venta.

        El criterio a seguir sera el de: P > MA[n] para buy signals y P<MA[n] para sell signals

        :param symbol:required
        :param interval: segundos que dejaremos pasar entre iteracion
        :param SMA_periods: n periodos de calculo del SMA
        :param save: Guardar los resultados en .csv
        """


        prev_signal = None
        MA = f"MA_{SMA_periods}"


        data = pd.DataFrame(columns=['price',MA,"signal"])
        results = pd.DataFrame(columns=['timestamp','signal','price','qty','total','fee','wallet']).set_index('timestamp')


        while self._Strategies__stop is None:
        
            #Obtenemos información del precio y construimos nuestro DF de evaluación de signals
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

            #Se establecen los desencadenantes
            if data.loc[timestamp,'signal'] == "buy" and prev_signal != "buy":

                price = data.loc[timestamp,"price"]
                prev_signal = data.loc[timestamp,"signal"]
                
                qty_buy = math.floor(self._Strategies__wallet/(price*0.00001))*0.00001
                total_buy = price * qty_buy
                fee_buy = total_buy*0.00100

                self._Strategies__wallet = qty_buy-(qty_buy*0.00100)

                dict={
                    'signal' : data.loc[timestamp,'signal'],
                    'price' : price,
                    'qty' : qty_buy,
                    'total': total_buy,
                    'fee' : fee_buy,
                    'wallet' : self._Strategies__wallet
                }
                results.loc[timestamp] = dict
                print(dict)

            elif data.loc[timestamp,'signal'] == "sell" and prev_signal not in ["sell",None]:
                    
                    price = data.loc[timestamp,"price"]
                    prev_signal = data.loc[timestamp,"signal"]
                    
                    qty_sell = round(self._Strategies__wallet,5)
                    total_sell = price * qty_sell
                    fee_sell = total_sell*0.00100

                    self._Strategies__wallet = total_sell - fee_sell

                    dict={
                        'signal' : data.loc[timestamp,'signal'],
                        'price' : price,
                        'qty' : qty_sell,
                        'total': total_sell,
                        'fee' : fee_sell,
                        'wallet' : self._Strategies__wallet
                    }
                    results.loc[timestamp]=dict
                    print(dict)

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


if __name__ == "__main__":

    Testing().cross_SMA(symbol="BTCUSDT",interval=1,SMA_periods=25,save=False)