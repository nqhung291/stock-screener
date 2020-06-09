def single_candle_reversal(doji: int, reversal_candle: dict, confirmation_candle: dict, ema: float):
    if doji and reversal_candle['low'] <= ema < min(reversal_candle['open'], reversal_candle['close']):
        return is_bullish_candle(confirmation_candle['open'], confirmation_candle['close']) \
                and confirmation_candle['low'] > reversal_candle['low'] \
                and confirmation_candle['close'] > reversal_candle['high']
    return False


def basic_two_candle_reversal(prev_reversal_low: float, reversal_candle: dict, confirmation_candle: dict, ema: float):
    if reversal_candle['low'] <= ema < min(reversal_candle['open'], reversal_candle['close']) \
            and reversal_candle['low'] < prev_reversal_low:
        return is_bullish_candle(confirmation_candle['open'], confirmation_candle['close']) \
                and confirmation_candle['low'] > reversal_candle['low'] \
                and confirmation_candle['close'] > reversal_candle['high']
    return False


def inside_bar_two_candle_reversal(prev_reversal: dict, reversal_candle: dict, confirmation_candle: dict, ema: float):
    if prev_reversal['low'] < reversal_candle['low'] < ema < min(reversal_candle['close'], reversal_candle['open']) \
            and prev_reversal['high'] > reversal_candle['high']:
        return is_bullish_candle(confirmation_candle['open'], confirmation_candle['close']) \
                and confirmation_candle['low'] > reversal_candle['low'] \
                and confirmation_candle['close'] > reversal_candle['high']
    return False


# def two_candle_reversal_trade_through(prev_reversal: dict, reversal_candle: dict, confirmation_candle: dict, ema: float):
#     if not is_bullish_candle(prev_reversal['open'], prev_reversal['close']) \
#             and is_bullish_candle(reversal_candle['open'], reversal_candle['close']) \
#             and prev_reversal['low'] > reversal_candle['low'] \
#             and prev_reversal['high'] > reversal_candle['high'] \
#             and :
#         return True
#
#     return False


def is_bullish_candle(open, close):
    return close > open

