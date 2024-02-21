import math

class Orders:

    def __init__(self) -> None:
        pass

    def make_order():
        pass

    def fake_order(signal,amount,lot_size,price,wallet):
        
        data = None

        if signal == "buy":
            qty_buy= math.floor(amount/(price*lot_size))*lot_size
            total_buy = price*qty_buy
            fee_buy = qty_buy * 0.00100 #USDT fee rate

            data = {
                "price":price,
                "qty":qty_buy,
                "total":total_buy,
                "fee":fee_buy,
                "type":signal
            }

        if signal == "sell":
            qty_sell = round(wallet,5)
            total_sell = price * qty_sell
            fee_sell = total_sell * 0.00100 #USDT fee rate

            data = {
                "price":price,
                "qty":qty_sell,
                "total":total_sell,
                "fee":fee_sell,
                "type":signal
            }

        else:
             data = {
                "price":price,
                "qty":None,
                "total":None,
                "fee":None,
                "type":None
            }

        return data
    
if __name__ == "__main__":
    order = Orders.fake_order(signal="NaN",amount=8,lot_size=0.00001,price=37323.22,wallet=0.00028350)
    print(order)