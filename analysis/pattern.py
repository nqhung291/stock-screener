def single_candle_reversal(doji: int, reversal_candle: dict, confirmation_candle: dict, ema: float) -> bool:
    if doji and reversal_candle['low'] <= ema < min(reversal_candle['open'], reversal_candle['close']):
        if is_bullish_candle(confirmation_candle['open'], confirmation_candle['close']) \
                and confirmation_candle['low'] > reversal_candle['low'] \
                and confirmation_candle['close'] > reversal_candle['high']:
            return True
    return False


def basic_two_candle_reversal(prev_reversal_low: float, reversal_candle: dict, confirmation_candle: dict, ema: float) -> bool:
    if reversal_candle['low'] <= ema < min(reversal_candle['open'], reversal_candle['close']) \
            and reversal_candle['low'] < prev_reversal_low:
        if is_bullish_candle(confirmation_candle['open'], confirmation_candle['close']) \
                and confirmation_candle['low'] > reversal_candle['low'] \
                and confirmation_candle['close'] > reversal_candle['high']:
            return True
    return False


def is_bullish_candle(open, close):
    return True if close > open else False
