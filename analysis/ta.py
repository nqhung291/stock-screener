from talib import abstract
from db import db
import numpy as np


def calculate_ema():
    for symbol in db.get_stock_symbol():
        (open, high, low, close) = db.get_price(symbol)
        ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)[-1]
        ema_50 = np.round(abstract.EMA(np.array(close), timeperiod=50), 4)[-1]
        ema_100 = np.round(abstract.EMA(np.array(close), timeperiod=100), 4)[-1]
        ema_150 = np.round(abstract.EMA(np.array(close), timeperiod=150), 4)[-1]
        ema_200 = np.round(abstract.EMA(np.array(close), timeperiod=200), 4)[-1]
        ema = (ema_18, ema_50, ema_100, ema_150, ema_200)
        print(symbol, ema)
