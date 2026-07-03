"""
MarketPulse AI — Technical Indicator Calculator
Computes RSI, MACD, Bollinger Bands, ATR, ADX, moving averages, support/resistance.
Uses only numpy/pandas — no LLM dependency.
"""
import math
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

def _mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)

def _std(values: List[float], mean_val: float) -> float:
    if not values:
        return 0.0
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

def compute_sma(prices: List[float], period: int) -> Optional[float]:
    """Simple Moving Average."""
    if len(prices) < period:
        return None
    return float(_mean(prices[-period:]))

def compute_ema(prices: List[float], period: int) -> Optional[float]:
    """Exponential Moving Average."""
    if len(prices) < period:
        return None
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = (price - ema) * multiplier + ema
    return float(ema)

def compute_rsi(prices: List[float], period: int = 14) -> Optional[float]:
    """Relative Strength Index (0-100)."""
    if len(prices) < period + 1:
        return None
    
    recent_prices = prices[-(period + 1):]
    deltas = [recent_prices[i+1] - recent_prices[i] for i in range(period)]
    
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]
    
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return float(100 - (100 / (1 + rs)))


def compute_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, Optional[float]]:
    """MACD, Signal Line, Histogram."""
    if len(prices) < slow + signal:
        return {"macd": None, "signal": None, "histogram": None}

    # Calculate EMAs
    fast_ema = compute_ema(prices, fast)
    slow_ema = compute_ema(prices, slow)

    if fast_ema is None or slow_ema is None:
        return {"macd": None, "signal": None, "histogram": None}

    macd_val = fast_ema - slow_ema

    # Approximate signal line (simplified for demo)
    macd_series = []
    for i in range(signal + slow, len(prices) + 1):
        fe = compute_ema(prices[:i], fast)
        se = compute_ema(prices[:i], slow)
        if fe and se:
            macd_series.append(fe - se)

    signal_val = compute_ema(macd_series, signal) if len(macd_series) >= signal else macd_val * 0.9
    histogram = macd_val - (signal_val or 0)

    return {
        "macd": round(macd_val, 6),
        "signal": round(signal_val, 6) if signal_val else None,
        "histogram": round(histogram, 6),
    }


def compute_bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> Dict[str, Optional[float]]:
    """Bollinger Bands."""
    if len(prices) < period:
        return {"upper": None, "middle": None, "lower": None}
    window = prices[-period:]
    middle = float(_mean(window))
    std = float(_std(window, middle))
    return {
        "upper": round(middle + std_dev * std, 6),
        "middle": round(middle, 6),
        "lower": round(middle - std_dev * std, 6),
    }


def compute_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
    """Average True Range."""
    if len(highs) < period + 1:
        return None
    true_ranges = []
    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1])
        )
        true_ranges.append(tr)
    return float(_mean(true_ranges[-period:]))


def compute_adx(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Dict[str, Optional[float]]:
    """Average Directional Index with +DI and -DI."""
    if len(highs) < period + 1:
        return {"adx": None, "plus_di": None, "minus_di": None}

    plus_dm_list = []
    minus_dm_list = []
    tr_list = []

    for i in range(1, len(highs)):
        plus_dm = highs[i] - highs[i - 1]
        minus_dm = lows[i - 1] - lows[i]

        if plus_dm > minus_dm and plus_dm > 0:
            plus_dm_list.append(plus_dm)
            minus_dm_list.append(0)
        elif minus_dm > plus_dm and minus_dm > 0:
            plus_dm_list.append(0)
            minus_dm_list.append(minus_dm)
        else:
            plus_dm_list.append(0)
            minus_dm_list.append(0)

        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1])
        )
        tr_list.append(tr)

    if len(tr_list) < period:
        return {"adx": None, "plus_di": None, "minus_di": None}

    atr = _mean(tr_list[-period:])
    if atr == 0:
        return {"adx": 0, "plus_di": 0, "minus_di": 0}

    plus_di = (_mean(plus_dm_list[-period:]) / atr) * 100
    minus_di = (_mean(minus_dm_list[-period:]) / atr) * 100

    dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 0
    adx = dx  # Simplified; full ADX uses smoothed DX

    return {
        "adx": round(float(adx), 2),
        "plus_di": round(float(plus_di), 2),
        "minus_di": round(float(minus_di), 2),
    }


def compute_support_resistance(highs: List[float], lows: List[float], closes: List[float]) -> Dict[str, Optional[float]]:
    """Pivot point support and resistance."""
    if not highs or not lows or not closes:
        return {"support_1": None, "resistance_1": None, "pivot": None}
    h = highs[-1]
    l = lows[-1]
    c = closes[-1]
    pivot = (h + l + c) / 3
    return {
        "pivot": round(pivot, 6),
        "support_1": round(2 * pivot - h, 6),
        "resistance_1": round(2 * pivot - l, 6),
    }


def compute_all_indicators(candles: List[Dict[str, Any]], interval: str = "1d") -> Dict[str, Any]:
    """Compute all technical indicators from candle data."""
    if not candles or len(candles) < 26:
        return {}

    closes = [float(c["close"]) for c in candles]
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    macd_result = compute_macd(closes)
    bb_result = compute_bollinger_bands(closes)
    adx_result = compute_adx(highs, lows, closes)
    sr_result = compute_support_resistance(highs, lows, closes)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "interval": interval,
        "sma_20": compute_sma(closes, 20),
        "sma_50": compute_sma(closes, 50),
        "sma_200": compute_sma(closes, 200),
        "ema_12": compute_ema(closes, 12),
        "ema_26": compute_ema(closes, 26),
        "rsi_14": compute_rsi(closes, 14),
        "macd": macd_result["macd"],
        "macd_signal": macd_result["signal"],
        "macd_histogram": macd_result["histogram"],
        "bb_upper": bb_result["upper"],
        "bb_middle": bb_result["middle"],
        "bb_lower": bb_result["lower"],
        "atr_14": compute_atr(highs, lows, closes, 14),
        "adx": adx_result["adx"],
        "plus_di": adx_result["plus_di"],
        "minus_di": adx_result["minus_di"],
        "support_1": sr_result["support_1"],
        "resistance_1": sr_result["resistance_1"],
        "pivot": sr_result["pivot"],
        "provider": "system_calculated",
        "data_freshness": "calculated",
    }


def compute_technical_score(indicators: Dict[str, Any], price: float) -> Dict[str, Any]:
    """
    Calculate a technical score from -100 to +100.
    Returns score + sub-scores for transparency.
    """
    if not indicators:
        return {"score": 0, "confidence": 0, "sub_scores": {}, "data_quality": 0}

    sub_scores = {}
    weights = {}

    # RSI Signal
    rsi = indicators.get("rsi_14")
    if rsi is not None:
        if rsi < 30:
            sub_scores["rsi"] = 60 + (30 - rsi) * 2  # Oversold = bullish
        elif rsi > 70:
            sub_scores["rsi"] = -(60 + (rsi - 70) * 2)  # Overbought = bearish
        elif rsi > 50:
            sub_scores["rsi"] = (rsi - 50) * 1.5
        else:
            sub_scores["rsi"] = (rsi - 50) * 1.5
        weights["rsi"] = 0.15

    # MACD Signal
    macd = indicators.get("macd")
    macd_signal = indicators.get("macd_signal")
    if macd is not None and macd_signal is not None:
        if macd > macd_signal:
            sub_scores["macd"] = min(50, (macd - macd_signal) / max(abs(macd), 0.001) * 100)
        else:
            sub_scores["macd"] = max(-50, (macd - macd_signal) / max(abs(macd), 0.001) * 100)
        weights["macd"] = 0.15

    # Moving Average Trend
    sma_20 = indicators.get("sma_20")
    sma_50 = indicators.get("sma_50")
    if sma_20 is not None and sma_50 is not None and price > 0:
        if price > sma_20 > sma_50:
            sub_scores["trend"] = 50  # Uptrend
        elif price < sma_20 < sma_50:
            sub_scores["trend"] = -50  # Downtrend
        elif price > sma_50:
            sub_scores["trend"] = 20
        else:
            sub_scores["trend"] = -20
        weights["trend"] = 0.20

    # Bollinger Band Position
    bb_upper = indicators.get("bb_upper")
    bb_lower = indicators.get("bb_lower")
    bb_middle = indicators.get("bb_middle")
    if bb_upper and bb_lower and bb_middle and price > 0:
        bb_width = bb_upper - bb_lower
        if bb_width > 0:
            position = (price - bb_lower) / bb_width
            if position > 0.9:
                sub_scores["bollinger"] = -30  # Near upper band
            elif position < 0.1:
                sub_scores["bollinger"] = 30  # Near lower band
            else:
                sub_scores["bollinger"] = (0.5 - position) * 40
            weights["bollinger"] = 0.10

    # ADX Trend Strength
    adx = indicators.get("adx")
    plus_di = indicators.get("plus_di")
    minus_di = indicators.get("minus_di")
    if adx is not None and plus_di is not None and minus_di is not None:
        if adx > 25:  # Strong trend
            direction = 1 if plus_di > minus_di else -1
            sub_scores["adx"] = direction * min(50, adx)
        else:
            sub_scores["adx"] = 0
        weights["adx"] = 0.15

    # Support/Resistance
    support = indicators.get("support_1")
    resistance = indicators.get("resistance_1")
    if support and resistance and price > 0:
        range_pct = (resistance - support) / price * 100
        position = (price - support) / max(resistance - support, 0.001)
        if position < 0.3:
            sub_scores["support_resistance"] = 25  # Near support
        elif position > 0.7:
            sub_scores["support_resistance"] = -25  # Near resistance
        else:
            sub_scores["support_resistance"] = 0
        weights["support_resistance"] = 0.10

    # Volume (placeholder - would use actual volume data)
    sub_scores["volume"] = 0
    weights["volume"] = 0.15

    # Calculate weighted score
    if not sub_scores:
        return {"score": 0, "confidence": 0, "sub_scores": {}, "data_quality": 0}

    total_weight = sum(weights.values())
    weighted_score = sum(
        sub_scores.get(k, 0) * weights.get(k, 0)
        for k in sub_scores
    ) / max(total_weight, 0.01)

    # Clamp to -100 to +100
    final_score = max(-100, min(100, weighted_score))

    # Data quality based on how many indicators we could compute
    data_quality = len(sub_scores) / 7 * 100

    # Confidence based on indicator agreement
    signs = [1 if v > 0 else (-1 if v < 0 else 0) for v in sub_scores.values()]
    if signs:
        agreement = abs(sum(signs)) / len(signs)
    else:
        agreement = 0

    return {
        "score": round(final_score, 2),
        "confidence": round(agreement * data_quality, 2),
        "sub_scores": {k: round(v, 2) for k, v in sub_scores.items()},
        "data_quality": round(data_quality, 2),
    }
