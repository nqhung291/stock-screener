from talib import abstract
from db import db
import numpy as np

prior_date = -1


def bounce_strategy():
    for symbol in db.get_stock_symbol():
        (open, high, low, close, date) = db.get_price(symbol)
        ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)[prior_date]
        ema_50 = np.round(abstract.EMA(np.array(close), timeperiod=50), 4)[prior_date]
        doji = abstract.CDLDOJI(np.array([open[prior_date]]),
                                np.array([high[prior_date]]),
                                np.array([low[prior_date]]),
                                np.array([close[prior_date]]))
        print(symbol, doji, (ema_18, ema_50))
        if doji[0] and low[prior_date] <= ema_18 < close[prior_date] and open[prior_date] > ema_18:
            print('Bounce 18', symbol, (close[prior_date]), (ema_18, ema_50), date[prior_date])

        if doji[0] and low[prior_date] <= ema_50 < close[prior_date] and open[prior_date] > ema_50:
            print('Bounce 50', symbol, (close[prior_date]), (ema_18, ema_50), date[prior_date])


def bounce_strategy_backtest():
    for symbol in db.get_stock_symbol():
        (open, high, low, close, date) = db.get_price(symbol)
        doji_list = abstract.CDLDOJI(np.array(open), np.array(high), np.array(low), np.array(close))
        for p_date in range(len(open)):
            ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)[p_date]
            ema_50 = np.round(abstract.EMA(np.array(close), timeperiod=50), 4)[p_date]

            if doji_list[p_date] and low[p_date] <= ema_18 < close[p_date] and open[p_date] > ema_18:
                print('Bounce 18', symbol, (close[p_date]), (ema_18, ema_50), date[p_date])

            if doji_list[p_date] and low[p_date] <= ema_50 < close[p_date] and open[p_date] > ema_50:
                print('Bounce 50', symbol, (close[p_date]), (ema_18, ema_50), date[p_date])
