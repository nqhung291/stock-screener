from talib import abstract
from db import db
import numpy as np
from analysis.pattern import *


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
            if i > 1:
                if single_candle_reversal(doji_list[i - 1], reversal_candle, confirmation_candle, ema_18):
                    print('Doji bounce 18 + confirmation', symbol, date[i])
                if single_candle_reversal(doji_list[i - 1], reversal_candle, confirmation_candle, ema_50):
                    print('Doji bounce 50 + confirmation', symbol, date[i])
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


if __name__ == '__main__':
    bounce_strategy_backtest()