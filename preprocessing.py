from mju_DL_project import get_stock_price

class Preprocessing():

    def __init__(self, code, name):
        self.name = name
        self.code = code
        self.data = get_stock_price.stock_price().get_price(code= code)
        self.low   = self.data["Low"]
        self.high  = self.data['High']
        self.close = self.data['Close']
        self.volume = self.data['Volume']
        self.change = self.data['Change']
    def get_


