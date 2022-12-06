# Stock Class
class Stock:
    def __init__(self,ticker,name,price,date,amount,invest_total):
        self.ticker = ticker
        self.name = name
        self.price = price
        self.date = date
        self.amount = amount
        self.invest_total = invest_total


class OrderFromUser:
    def __init__(self,ticker,name,price,date,amount,order_kind):
        self.ticker = ticker
        self.name = name
        self.price = price
        self.date = date
        self.amount = amount
        self.order_kind = order_kind
