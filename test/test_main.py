from talib import abstract
from db import db
import numpy as np
from analysis.pattern import *


def bounce_strategy_backtest():
    for symbol in db.get_stock_symbol():
        (open, high, low, close, date) = db.get_price(symbol)
        doji_list = abstract.CDLDOJI(np.array(open), np.array(high), np.array(low), np.array(close))
        macd, macdsignal, macdhist = abstract.MACD(np.array(close), fastperiod=50, slowperiod=100, signalperiod=9)
        slowk, slowd = abstract.STOCH(np.array(high), np.array(low), np.array(close), fastk_period=5, slowk_period=3,
                                      slowk_matype=0, slowd_period=3, slowd_matype=0)
        list_ema_18 = np.round(abstract.EMA(np.array(close), timeperiod=18), 4)
        list_ema_50 = np.round(abstract.EMA(np.array(close), timeperiod=50), 4)

        for i in range(1, len(date)):
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
                candle_pattern = False
                if single_candle_reversal(doji_list[i - 1], reversal_candle, confirmation_candle, ema_18):
                    candle_pattern = True
                    # print('Doji bounce 18 + confirmation', symbol, date[i])
                if single_candle_reversal(doji_list[i - 1], reversal_candle, confirmation_candle, ema_50):
                    candle_pattern = True
                    # print('Doji bounce 50 + confirmation', symbol, date[i])
                else:
                    if basic_two_candle_reversal(
                            prev_reversal['low'], reversal_candle, confirmation_candle, ema_18
                    ):
                        candle_pattern = True
                        # print('2 Candle reversal + Confirmation 18', symbol, date[i])
                    if basic_two_candle_reversal(
                            prev_reversal['low'], reversal_candle, confirmation_candle, ema_50
                    ):
                        candle_pattern = True
                        # print('2 Candle reversal + Confirmation 50', symbol, date[i])
                    else:
                        if inside_bar_two_candle_reversal(
                                prev_reversal, reversal_candle, confirmation_candle, ema_18
                        ):
                            candle_pattern = True
                            # print('2 Candle reversal inside bar + Confirmation 18', symbol, date[i])
                        if inside_bar_two_candle_reversal(
                                prev_reversal, reversal_candle, confirmation_candle, ema_50
                        ):
                            candle_pattern = True
                            # print('2 Candle reversal inside bar + Confirmation 50', symbol, date[i])
                if candle_pattern is True:
                    if slowk[i] < 30:
                        enter_trade = False
                        if macd[i] > macdsignal[i]:  # if macd is bullish
                            enter_trade = True
                        else:
                            macd_period = macd[i-4:i+1]
                            macd_signal_period = macdsignal[i-4:i+1]
                            if not np.isnan(macd_period).any() \
                                    and not np.isnan(macd_signal_period).any() \
                                    and macd_period < macd_signal_period:
                                print('bearish enter trade')
                                enter_trade = True

                        if enter_trade:
                            sl = confirmation_candle['low'] - 0.05
                            entry = confirmation_candle['high'] + 0.05
                            tp = entry + (entry - sl) * 2
                            print('Enter ', symbol, date[i], (np.round(sl, 2), np.round(entry, 2), np.round(tp, 2)))


if __name__ == '__main__':
    bounce_strategy_backtest()
