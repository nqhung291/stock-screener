from talib import abstract
from db import db
import numpy as np
from analysis.pattern import *
from datetime import date
import datetime
today = -1


def screener(end_date=date.today()):
    if type(end_date) is str:
        end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y').date()

    bounce_watch_dict = {}
    bounce_enter_dict = {}
    ip_watch_dict = {}
    ip_enter_dict = {}
    for (symbol, exchange) in db.get_stock_symbol():
        open, high, low, close, date = db.get_price(symbol, end_date)
        result = bounce_strategy(symbol, open, high, low, close)
        if result and result[1] == 'watch':
            bounce_watch_list = bounce_watch_dict.get(exchange, [])
            bounce_watch_list.append(symbol)
            bounce_watch_dict[exchange] = bounce_watch_list
        elif result and result[1] == 'enter':
            bounce_enter_list = bounce_enter_dict.get(exchange, [])
            bounce_enter_list.append(symbol)
            bounce_enter_dict[exchange] = bounce_enter_list

        result = impulse_pullback(symbol, open, high, low, close)
        if result and result[1] == 'watch':
            ip_watch_list = ip_watch_dict.get(exchange, [])
            ip_watch_list.append(symbol)
            ip_watch_dict[exchange] = ip_watch_list
        elif result and result[1] == 'enter':
            ip_enter_list = ip_enter_dict.get(exchange, [])
            ip_enter_list.append(symbol)
            ip_enter_dict[exchange] = ip_enter_list
    return bounce_watch_dict, bounce_enter_dict, ip_watch_dict, ip_enter_dict


def bounce_strategy(symbol, open, high, low, close):
    result = None
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
    indicator = False

    if single_candle_reversal(reversal_candle, ema_18):
        candle_pattern = True
    if single_candle_reversal(reversal_candle, ema_50):
        candle_pattern = True
    if doji_candle_reversal(doji_list[today], reversal_candle, ema_18):
        candle_pattern = True
    if doji_candle_reversal(doji_list[today], reversal_candle, ema_50):
        candle_pattern = True
    else:
        if basic_two_candle_reversal(prev_reversal['low'], reversal_candle, ema_18):
            candle_pattern = True
        if basic_two_candle_reversal(prev_reversal['low'], reversal_candle, ema_50):
            candle_pattern = True
        else:
            if inside_bar_two_candle_reversal(prev_reversal, reversal_candle, ema_18):
                candle_pattern = True
            if inside_bar_two_candle_reversal(prev_reversal, reversal_candle, ema_50):
                candle_pattern = True
            if two_candle_reversal_trade_through(prev_reversal, reversal_candle, ema_18):
                candle_pattern = True
            if two_candle_reversal_trade_through(prev_reversal, reversal_candle, ema_50):
                candle_pattern = True

    if candle_pattern is True:
        if slowk[today] < 30:
            if macd[today] > macdsignal[today]:  # if macd is bullish
                indicator = True
            else:  # macd is bearish and not crossed bullish less than 5 days
                macd_period = macd[today - 4:]
                macd_signal_period = macdsignal[today - 4:]
                if not np.isnan(macd_period).any() \
                        and not np.isnan(macd_signal_period).any() \
                        and np.all([i < j for i, j in zip(macd_period, macd_signal_period)]):
                    indicator = True
    if indicator:
        result = (symbol, 'watch')
        if is_confirmation_candle(reversal_candle, confirmation_candle):
            result = (symbol, 'enter')
    return result


def impulse_pullback(symbol, open, high, low, close):
    num_prev_day = -4
    ema_6 = np.round(abstract.EMA(np.array(close), timeperiod=6), 4)[num_prev_day:]
    ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)[num_prev_day:]
    macd_all, macdsignal_all, macdhist_all = abstract.MACD(np.array(close), fastperiod=12, slowperiod=26, signalperiod=9)
    macd = macd_all[num_prev_day:]
    macdsignal = macdsignal_all[num_prev_day:]
    result = None
    swing_high_ema = None
    swing_high_macd = None

    if not np.isnan(ema_6).any() and not np.isnan(ema_18).any() and not np.isnan(macd).any() and not np.isnan(macdsignal).any():
        for prev_date in range(-2, num_prev_day - 1, -1):
            if swing_high_ema is None and ema_6[-1] > ema_18[-1] and ema_6[prev_date] <= ema_18[prev_date]:
                swing_high_ema = prev_date + 1
            if swing_high_macd is None and macd[-1] > macdsignal[-1] and macd[prev_date] <= macdsignal[prev_date]:
                swing_high_macd = prev_date + 1

    today_candle = {
        'high': high[-1],
        'low': low[-1]
    }
    swing_high_prev_candle = {
        'high': high[-2],
        'low': low[-2]
    }
    if (swing_high_ema == -1 or swing_high_macd == -1) and is_higher_candle(swing_high_prev_candle, today_candle):
        return symbol, 'watch'

    if swing_high_ema is not None:
        ema_sw_candle = {
            'high': high[swing_high_ema],
            'low': low[swing_high_ema]
        }
        if high[swing_high_ema] > high[swing_high_ema - 1] \
                and all(high[swing_high_ema] > i for i in high[swing_high_ema + 1:-1]) \
                and is_pullback_candle(ema_sw_candle, today_candle):
            result = (symbol, 'enter')

    if swing_high_macd is not None:
        macd_sw_candle = {
            'high': high[swing_high_macd],
            'low': low[swing_high_macd]
        }
        if high[swing_high_macd] > high[swing_high_macd - 1] \
                and all(high[swing_high_macd] > i for i in high[swing_high_macd + 1:-1]) \
                and is_pullback_candle(macd_sw_candle, today_candle):
            result = (symbol, 'enter')

    return result
