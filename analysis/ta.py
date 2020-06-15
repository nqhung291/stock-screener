from talib import abstract
from db import db
import numpy as np
from analysis.pattern import *
from datetime import datetime

today = -1


def bounce_strategy(end_date):
    enter_stock_list = []
    for symbol in db.get_stock_symbol():
        (open, high, low, close, date) = db.get_price(symbol, end_date)
        doji_list = abstract.CDLDOJI(np.array(open), np.array(high), np.array(low), np.array(close))
        ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)[today]
        ema_50 = np.round(abstract.EMA(np.array(close), timeperiod=50), 4)[today]
        macd, macdsignal, macdhist = abstract.MACD(np.array(close), fastperiod=50, slowperiod=100, signalperiod=9)
        slowk, slowd = abstract.STOCH(np.array(high), np.array(low), np.array(close), fastk_period=5, slowk_period=3,
                                      slowk_matype=0, slowd_period=3, slowd_matype=0)
        prev_reversal = {
            'open': open[today - 2],
            'high': high[today - 2],
            'low': low[today - 2],
            'close': close[today - 2],
        }
        reversal_candle = {
            'open': open[today - 1],
            'high': high[today - 1],
            'low': low[today - 1],
            'close': close[today - 1],
        }
        confirmation_candle = {
            'open': open[today],
            'high': high[today],
            'low': low[today],
            'close': close[today],
        }

        candle_pattern = False
        enter_trade = False

        if single_candle_reversal(reversal_candle, confirmation_candle, ema_18):
            candle_pattern = True
            # print('Single candle bounce 18 + confirmation', symbol, date[today])
        if single_candle_reversal(reversal_candle, confirmation_candle, ema_50):
            candle_pattern = True
            # print('Single candle bounce 50 + confirmation', symbol, date[today])
        if doji_candle_reversal(doji_list[today], reversal_candle, confirmation_candle, ema_18):
            candle_pattern = True
            # print('Doji candle bounce 18 + confirmation', symbol, date[today])
        if doji_candle_reversal(doji_list[today], reversal_candle, confirmation_candle, ema_50):
            candle_pattern = True
            # print('Doji candle bounce 50 + confirmation', symbol, date[today])
        else:
            if basic_two_candle_reversal(
                    prev_reversal['low'], reversal_candle, confirmation_candle, ema_18
            ):
                candle_pattern = True
                # print('2 Candle reversal + Confirmation 18', symbol, date[today])
            if basic_two_candle_reversal(
                    prev_reversal['low'], reversal_candle, confirmation_candle, ema_50
            ):
                candle_pattern = True
                # print('2 Candle reversal + Confirmation 50', symbol, date[today])
            else:
                if inside_bar_two_candle_reversal(
                        prev_reversal, reversal_candle, confirmation_candle, ema_18
                ):
                    candle_pattern = True
                    # print('2 Candle reversal inside bar + Confirmation 18', symbol, date[today])
                if inside_bar_two_candle_reversal(
                        prev_reversal, reversal_candle, confirmation_candle, ema_50
                ):
                    candle_pattern = True
                    # print('2 Candle reversal inside bar + Confirmation 50', symbol, date[today])
                if two_candle_reversal_trade_through(
                        prev_reversal, reversal_candle, confirmation_candle, ema_18
                ):
                    candle_pattern = True
                if two_candle_reversal_trade_through(
                        prev_reversal, reversal_candle, confirmation_candle, ema_50
                ):
                    candle_pattern = True

        if candle_pattern is True:
            if slowk[today] < 30:
                if macd[today] > macdsignal[today]:  # if macd is bullish
                    enter_trade = True
                else:
                    macd_period = macd[today - 4:]
                    macd_signal_period = macdsignal[today - 4:]
                    if not np.isnan(macd_period).any() \
                            and not np.isnan(macd_signal_period).any() \
                            and np.all(macd_period < macd_signal_period):
                        enter_trade = True
                if enter_trade:
                    sl = np.round(confirmation_candle['low'] - 0.05, 2)
                    entry = np.round(confirmation_candle['high'] + 0.05, 2)
                    tp = np.round(entry + (entry - sl) * 2, 2)
                    signal = f'Enter {symbol} {date[today]} | sl: {sl} | entry: {entry} | tp: {tp}'
                    enter_stock_list.append(signal)
    return enter_stock_list

