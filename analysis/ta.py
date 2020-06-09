from talib import abstract
from db import db
import numpy as np
from analysis.pattern import *

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
        list_ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)
        list_ema_50 = np.round(abstract.EMA(np.array(close), timeperiod=50), 4)

        for i in range(1, len(open)):
            ema_18 = list_ema_18[i]
            ema_50 = list_ema_50[i]
            prev_reversal = {
                'open': open[i - 2],
                'high': high[i - 2],
                'low': low[i - 2],
                'close': close[i - 2],
            }
            reversal_candle = {
                'open': open[i - 1],
                'high': high[i - 1],
                'low': low[i - 1],
                'close': close[i - 1],
            }
            confirmation_candle = {
                'open': open[i],
                'high': high[i],
                'low': low[i],
                'close': close[i],
            }

            if single_candle_reversal(doji_list[i], reversal_candle, confirmation_candle, ema_18):
                print('Single candle bounce 18 + confirmation', symbol, date[i])
            if single_candle_reversal(doji_list[i], reversal_candle, confirmation_candle, ema_50):
                print('Single candle bounce 50 + confirmation', symbol, date[i])

            # double candle reversal pattern
            if i > 1:
                if basic_two_candle_reversal(
                    prev_reversal['low'], reversal_candle, confirmation_candle, ema_18
                ):
                    print('2 Candle reversal + Confirmation 18', symbol, date[i])
                if basic_two_candle_reversal(
                    prev_reversal['low'], reversal_candle, confirmation_candle, ema_50
                ):
                    print('2 Candle reversal + Confirmation 50', symbol, date[i])
                if inside_bar_two_candle_reversal(
                    prev_reversal, reversal_candle, confirmation_candle, ema_18
                ):
                    print('2 Candle reversal inside bar + Confirmation 18', symbol, date[i])
                if inside_bar_two_candle_reversal(
                        prev_reversal, reversal_candle, confirmation_candle, ema_50
                ):
                    print('2 Candle reversal inside bar + Confirmation 50', symbol, date[i])

