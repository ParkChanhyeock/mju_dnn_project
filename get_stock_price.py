import FinanceDataReader as fdr
import talib as ta
import pandas as pd
from scipy.interpolate import interp1d
import numpy as np

class stock_price:
    def __init__(self, code, start = "2018-12-01", end = "2020-05-29"): # 이동평균
        self.start = start
        self.end   = end
        self.code  = code


    def get_price(self):

        # 가격 불러오기
        price = fdr.DataReader(symbol = self.code,
                               start  = self.start,
                               end    = self.end)

        # 가격
        self.data = price
        self.low = self.data["Low"]       # 저가
        self.high = self.data['High']     # 고가
        self.close = self.data['Close']   # 종가
        self.volume = self.data['Volume'] # 거래량
        self.change = self.data['Change'] # 변화율
        # MACD
        self.macd,self.signal, _ = ta.MACD(self.close, fastperiod = 12, slowperiod = 26, signalperiod = 9)

        # 스토캐스틱 슬로우
        self.stok, self.stod = ta.STOCH(self.high, self.low, self.close,
                                          fastk_period=10 ,
                                          slowk_period=6,
                                          slowd_period=6)
        # 이동평균선 5,10,20 일
        self.data["ma5"]  = ta.SMA(self.close, timeperiod = 5)
        self.data["ma10"] = ta.SMA(self.close, timeperiod = 10)
        self.data['ma20'] = ta.SMA(self.close, timeperiod = 20)

        # RSI
        self.data['rsi'] = ta.RSI(self.close, timeperiod = 14)

        # VIX
        vix = fdr.DataReader("VIX", start = self.start, end = self.end)
        vix.rename(columns = {'Close' : 'vix'}, inplace = True)
        self.data = pd.merge(self.data, vix['vix'], left_index=True, right_index=True,how = 'left')
        # S&P 500
        snp = fdr.DataReader('US500', start = self.start, end = self.end)
        snp.rename(columns = {'Close' : 'snp'}, inplace = True)
        self.data = pd.merge(self.data, snp['snp'], left_index=True,right_index=True,how = 'left')
        # 환율
        ex  = fdr.DataReader("USD/KRW", start = self.start, end = self.end)
        ex.rename(columns={'Close': 'ex'}, inplace=True)
        self.data = pd.merge(self.data, ex['ex'], left_index=True,right_index=True,how = 'left')

    def Preprocessing(self):
        self.get_price()

        # 선형 보간법으로 결측치 처리
        for idx in ['vix','snp','ex'] :
            self.data[idx] = self.data[idx].interpolate(method = 'time')

        # MinMax Scale
        features = self.data.drop('Close', axis = 1)
        target   = self.data['Close']

        features = (features - np.min(features)) / (np.max(features) - np.min(features))

        features = features.loc["20190101":"20200531"]
        target   = target.loc["20190101":"20200531"]
        price    = pd.merge(features, target, left_index=True, right_index=True, how = 'left')
        return  price

code_dic = {"KS200": "KOSPI",
        "005930":"SAMSUNG",
        "000660":"SKhynix",
        "207940":"SAMBI",
        "035420":'NAVER',
        "068270":"CELLTRION"}

for code in code_dic:
    print(code)
    price = stock_price(code = code).Preprocessing()
    price.to_csv("{}.csv".format(code_dic[code]), index = True)

