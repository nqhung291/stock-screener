def single_candle_reversal(reversal_candle: dict, ema: float):
    return reversal_candle['low'] <= ema < min(reversal_candle['open'], reversal_candle['close'])


def doji_candle_reversal(doji: int, reversal_candle: dict, ema: float):
    return doji and reversal_candle['low'] <= ema < min(reversal_candle['open'], reversal_candle['close'])


def basic_two_candle_reversal(prev_reversal_low: float, reversal_candle: dict, ema: float):
    return reversal_candle['low'] <= ema < min(reversal_candle['open'], reversal_candle['close']) \
            and reversal_candle['low'] < prev_reversal_low


def inside_bar_two_candle_reversal(prev_reversal: dict, reversal_candle: dict, ema: float):
    return prev_reversal['low'] < reversal_candle['low'] < ema < min(reversal_candle['close'], reversal_candle['open']) \
            and prev_reversal['high'] > reversal_candle['high']


def two_candle_reversal_trade_through(prev_reversal: dict, reversal_candle: dict, ema: float):
    return not is_bullish_candle(prev_reversal['open'], prev_reversal['close']) \
            and prev_reversal['close'] <= ema <= prev_reversal['open'] \
            and is_bullish_candle(reversal_candle['open'], reversal_candle['close']) \
            and reversal_candle['open'] <= ema <= reversal_candle['close'] \
            and prev_reversal['low'] > reversal_candle['low']


def is_confirmation_candle(reversal_candle: dict, confirmation_candle: dict):
    return is_bullish_candle(confirmation_candle['open'], confirmation_candle['close']) \
           and confirmation_candle['low'] > reversal_candle['low'] \
           and confirmation_candle['close'] >= reversal_candle['high']


def is_bullish_candle(open, close):
    return close > open

