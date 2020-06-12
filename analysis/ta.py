from talib import abstract
from db import db
import numpy as np
from analysis.pattern import *

prior_date = -1


def bounce_strategy():
    for symbol in db.get_stock_symbol():
        (open, high, low, close, date) = db.get_price(symbol)
        doji_list = abstract.CDLDOJI(np.array(open), np.array(high), np.array(low), np.array(close))
        ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)[prior_date]
        ema_50 = np.round(abstract.EMA(np.array(close), timeperiod=50), 4)[prior_date]
        prev_reversal = {
            'open': open[prior_date - 2],
            'high': high[prior_date - 2],
            'low': low[prior_date - 2],
            'close': close[prior_date - 2],
        }
        reversal_candle = {
            'open': open[prior_date - 1],
            'high': high[prior_date - 1],
            'low': low[prior_date - 1],
            'close': close[prior_date - 1],
        }
        confirmation_candle = {
            'open': open[prior_date],
            'high': high[prior_date],
            'low': low[prior_date],
            'close': close[prior_date],
        }
        if single_candle_reversal(doji_list[prior_date - 1], reversal_candle, confirmation_candle, ema_18):
            print('Doji bounce 18 + confirmation', symbol, date[prior_date])
        if single_candle_reversal(doji_list[prior_date - 1], reversal_candle, confirmation_candle, ema_50):
            print('Doji bounce 50 + confirmation', symbol, date[prior_date])
        if basic_two_candle_reversal(
                prev_reversal['low'], reversal_candle, confirmation_candle, ema_18
        ):
            print('2 Candle reversal + Confirmation 18', symbol, date[prior_date])
        if basic_two_candle_reversal(
                prev_reversal['low'], reversal_candle, confirmation_candle, ema_50
        ):
            print('2 Candle reversal + Confirmation 50', symbol, date[prior_date])
        if inside_bar_two_candle_reversal(
                prev_reversal, reversal_candle, confirmation_candle, ema_18
        ):
            print('2 Candle reversal inside bar + Confirmation 18', symbol, date[prior_date])
        if inside_bar_two_candle_reversal(
                prev_reversal, reversal_candle, confirmation_candle, ema_50
        ):
            print('2 Candle reversal inside bar + Confirmation 50', symbol, date[prior_date])



