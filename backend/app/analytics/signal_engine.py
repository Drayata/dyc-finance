"""
MarketPulse AI — Signal Generation Engine
Hybrid scoring model combining technical, fundamental, news, and market context.
This is NOT an LLM-based prediction — it uses configurable weighted scoring.
"""
import random
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any

from app.analytics.technical import compute_all_indicators, compute_technical_score


# ==============================================================================
# Signal Classification Thresholds
# ==============================================================================

STOCK_THRESHOLDS = {
    "strong_bullish": (70, 100),
    "bullish": (35, 69),
    "neutral": (-34, 34),
    "bearish": (-69, -35),
    "strong_bearish": (-100, -70),
}

CRYPTO_THRESHOLDS = {
    "strong_bullish": (70, 100),
    "bullish": (35, 69),
    "neutral": (-34, 34),
    "bearish": (-69, -35),
    "strong_bearish": (-100, -70),
}

# Default component weights (configurable, documented as non-optimal)
STOCK_WEIGHTS = {
    "technical": 0.30,
    "fundamental": 0.25,
    "news": 0.25,
    "market_context": 0.10,
    "liquidity_quality": 0.10,
}

CRYPTO_WEIGHTS = {
    "technical": 0.30,
    "onchain": 0.25,
    "news": 0.25,
    "derivatives": 0.10,
    "liquidity_quality": 0.10,
}

# Disclaimer attached to every signal
SIGNAL_DISCLAIMER = (
    "This analytical signal is for educational and market-analysis purposes only. "
    "It does not constitute personalized investment advice and does not consider the "
    "financial condition, investment objectives, or risk profile of any individual user. "
    "All signals are probabilistic and do not guarantee future performance. "
    "Users remain fully responsible for their own investment decisions."
)


def classify_signal(score: float, asset_type: str = "stock") -> str:
    """Classify a numerical score into signal direction."""
    thresholds = STOCK_THRESHOLDS if asset_type == "stock" else CRYPTO_THRESHOLDS
    for direction, (low, high) in thresholds.items():
        if low <= score <= high:
            return direction
    return "neutral"


def compute_risk_level(volatility: float, liquidity: str, data_quality: float, market_regime: str) -> Dict[str, Any]:
    """Compute risk level based on multiple factors."""
    risk_score = 0

    # Volatility contribution
    if volatility > 0.05:
        risk_score += 30
    elif volatility > 0.03:
        risk_score += 15
    else:
        risk_score += 5

    # Liquidity contribution
    liquidity_scores = {"high": 0, "medium": 10, "low": 25, "very_low": 40}
    risk_score += liquidity_scores.get(liquidity, 15)

    # Data quality contribution
    if data_quality < 30:
        risk_score += 30
    elif data_quality < 50:
        risk_score += 15
    elif data_quality < 70:
        risk_score += 5

    # Market regime contribution
    regime_scores = {
        "bullish_trend": 0, "bearish_trend": 15, "sideways": 5,
        "high_volatility": 25, "crisis": 40, "risk_off": 20, "risk_on": 0,
    }
    risk_score += regime_scores.get(market_regime, 10)

    # Classify
    if risk_score >= 80:
        level = "extreme"
    elif risk_score >= 60:
        level = "very_high"
    elif risk_score >= 40:
        level = "high"
    elif risk_score >= 25:
        level = "medium"
    elif risk_score >= 10:
        level = "low"
    else:
        level = "very_low"

    return {"risk_level": level, "risk_score": risk_score}


def compute_confidence(
    indicator_agreement: float,
    data_quality: float,
    data_completeness: float,
    signal_stability: float,
    source_count: int,
    market_conditions: str,
) -> float:
    """
    Calculate confidence score (0-100).
    Confidence ≠ probability of profit. It measures evidence strength.
    """
    confidence = 0

    # Indicator agreement (0-1) → contributes up to 30
    confidence += indicator_agreement * 30

    # Data quality (0-100) → contributes up to 25
    confidence += (data_quality / 100) * 25

    # Data completeness (0-1) → contributes up to 15
    confidence += data_completeness * 15

    # Signal stability (0-1) → contributes up to 15
    confidence += signal_stability * 15

    # Multiple independent sources → contributes up to 10
    source_factor = min(source_count / 5, 1.0)
    confidence += source_factor * 10

    # Market condition penalty
    condition_penalties = {
        "normal": 0, "risk_on": 0, "sideways": -2,
        "high_volatility": -10, "crisis": -20, "risk_off": -5,
    }
    confidence += condition_penalties.get(market_conditions, -5)

    # Additional penalty: cap at 5
    confidence += 5

    return max(0, min(100, round(confidence, 1)))


def compute_expected_range(price: float, atr: Optional[float], volatility: float, time_horizon_days: int) -> Dict[str, float]:
    """
    Compute expected movement range. Uses ATR and historical volatility.
    Returns percentage range, NOT a guaranteed target.
    """
    if atr and price > 0:
        daily_move_pct = (atr / price) * 100
    else:
        daily_move_pct = volatility * 100

    # Scale by time horizon (sqrt of time for random walk approximation)
    import math
    horizon_factor = math.sqrt(time_horizon_days)

    move_pct = daily_move_pct * horizon_factor

    # Asymmetric range (slight upward bias for stocks historically)
    return {
        "low": round(-move_pct * 1.1, 2),
        "high": round(move_pct * 1.0, 2),
    }


def generate_signal_for_asset(
    symbol: str,
    asset_type: str,
    candles: List[Dict[str, Any]],
    news_data: List[Dict[str, Any]] = None,
    fundamental_data: Dict[str, Any] = None,
    onchain_data: Dict[str, Any] = None,
    market_regime: str = "sideways",
) -> Dict[str, Any]:
    """
    Generate a complete signal for an asset using hybrid scoring.
    This function orchestrates all scoring components.
    """
    now = datetime.now(timezone.utc)

    if not candles or len(candles) < 26:
        return {
            "error": "Insufficient historical data for signal generation",
            "data_quality_score": 0,
        }

    price = float(candles[-1]["close"])

    # --- Technical Score ---
    indicators = compute_all_indicators(candles)
    tech_result = compute_technical_score(indicators, price)
    technical_score = tech_result["score"]

    # --- News/Event Score ---
    news_score = 0
    news_factors = []
    if news_data:
        sentiments = [n.get("overall_sentiment", 0) for n in news_data if n.get("overall_sentiment") is not None]
        impacts = [n.get("impact_score", 0) for n in news_data if n.get("impact_score") is not None]

        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            news_score = avg_sentiment * 60  # Scale -1..+1 to -60..+60

        # Boost/penalize for high-impact news
        if impacts:
            avg_impact = sum(impacts) / len(impacts)
            if avg_impact > 70:
                # Amplify in the direction of sentiment
                direction_multiplier = 1.2 if news_score > 0 else 1.3
                news_score *= direction_multiplier

        for n in news_data[:3]:
            news_factors.append({
                "title": n.get("title", ""),
                "sentiment": n.get("overall_sentiment"),
                "impact": n.get("impact_score"),
                "direction": n.get("impact_direction"),
            })

    # --- Fundamental Score (stocks only) ---
    fundamental_score = 0
    if asset_type == "stock" and fundamental_data:
        pe = fundamental_data.get("pe_ratio")
        roe = fundamental_data.get("roe")
        growth = fundamental_data.get("revenue_growth_yoy")

        if pe is not None:
            if pe < 15:
                fundamental_score += 20
            elif pe > 30:
                fundamental_score -= 15

        if roe is not None:
            if roe > 20:
                fundamental_score += 15
            elif roe < 5:
                fundamental_score -= 10

        if growth is not None:
            if growth > 15:
                fundamental_score += 20
            elif growth < 0:
                fundamental_score -= 15

    # --- On-chain Score (crypto only) ---
    onchain_score = 0
    if asset_type == "crypto" and onchain_data:
        # Exchange flow (outflow > inflow = bullish supply squeeze)
        inflow = onchain_data.get("exchange_inflow", 0)
        outflow = onchain_data.get("exchange_outflow", 0)
        if outflow > inflow * 1.2:
            onchain_score += 20
        elif inflow > outflow * 1.2:
            onchain_score -= 15

        # Active addresses
        active = onchain_data.get("active_addresses", 0)
        if active > 500000:
            onchain_score += 10

        # Developer activity
        dev = onchain_data.get("developer_activity", 0)
        if dev > 70:
            onchain_score += 10

    # --- Market Context Score ---
    market_context_score = 0
    regime_scores = {
        "bullish_trend": 30, "risk_on": 20, "sideways": 0,
        "bearish_trend": -30, "risk_off": -20,
        "high_volatility": -10, "crisis": -40,
    }
    market_context_score = regime_scores.get(market_regime, 0)

    # --- Liquidity & Data Quality Score ---
    data_quality = tech_result.get("data_quality", 50)
    liquidity_quality_score = data_quality * 0.5

    # --- Risk Penalty ---
    atr = indicators.get("atr_14")
    volatility = (atr / price) if atr and price > 0 else 0.025
    risk_result = compute_risk_level(volatility, "medium", data_quality, market_regime)
    risk_penalty = risk_result["risk_score"] * 0.3

    # --- Combined Score ---
    weights = STOCK_WEIGHTS if asset_type == "stock" else CRYPTO_WEIGHTS

    if asset_type == "stock":
        final_score = (
            technical_score * weights["technical"]
            + fundamental_score * weights["fundamental"]
            + news_score * weights["news"]
            + market_context_score * weights["market_context"]
            + liquidity_quality_score * weights["liquidity_quality"]
            - risk_penalty
        )
    else:
        final_score = (
            technical_score * weights["technical"]
            + onchain_score * weights["onchain"]
            + news_score * weights["news"]
            + market_context_score * weights.get("derivatives", 0.10) * 10  # Placeholder
            + liquidity_quality_score * weights["liquidity_quality"]
            - risk_penalty
        )

    final_score = max(-100, min(100, final_score))

    # --- Signal Direction ---
    direction = classify_signal(final_score, asset_type)

    # --- Confidence ---
    confidence = compute_confidence(
        indicator_agreement=tech_result.get("confidence", 50) / 100,
        data_quality=data_quality,
        data_completeness=0.75 if news_data else 0.50,
        signal_stability=0.70,
        source_count=len(news_data) if news_data else 1,
        market_conditions="normal",
    )

    # --- Expected Range ---
    time_horizon_days = 7  # Default short-term
    time_horizon = "short_term"
    if abs(final_score) < 20:
        time_horizon = "swing"
        time_horizon_days = 21
    elif abs(final_score) > 60:
        time_horizon = "immediate"
        time_horizon_days = 1

    expected_range = compute_expected_range(price, atr, volatility, time_horizon_days)

    # --- Bull/Bear Factors ---
    bull_factors = []
    bear_factors = []
    key_risks = []

    # From technical
    rsi = indicators.get("rsi_14")
    if rsi and rsi < 40:
        bull_factors.append({"factor": f"RSI at {rsi:.1f} indicates potential oversold conditions", "type": "technical", "source": "system_calculated"})
    elif rsi and rsi > 60:
        bear_factors.append({"factor": f"RSI at {rsi:.1f} indicates potential overbought conditions", "type": "technical", "source": "system_calculated"})

    sma_20 = indicators.get("sma_20")
    sma_50 = indicators.get("sma_50")
    if sma_20 and sma_50:
        if price > sma_20 > sma_50:
            bull_factors.append({"factor": "Price above both 20-day and 50-day moving averages (uptrend)", "type": "technical", "source": "system_calculated"})
        elif price < sma_20 < sma_50:
            bear_factors.append({"factor": "Price below both 20-day and 50-day moving averages (downtrend)", "type": "technical", "source": "system_calculated"})

    # From news
    if news_data:
        for n in news_data[:2]:
            sent = n.get("overall_sentiment", 0)
            if sent > 0.3:
                bull_factors.append({"factor": n.get("title", "Positive news"), "type": "news", "source": n.get("source_name", "demo_mock")})
            elif sent < -0.3:
                bear_factors.append({"factor": n.get("title", "Negative news"), "type": "news", "source": n.get("source_name", "demo_mock")})

    # Always add risks
    key_risks.append({"risk": "Signal based on historical patterns that may not repeat", "severity": "medium"})
    if volatility > 0.03:
        key_risks.append({"risk": f"High daily volatility ({volatility*100:.1f}%) increases downside risk", "severity": "high"})
    key_risks.append({"risk": "External events (geopolitical, regulatory) can invalidate technical analysis", "severity": "medium"})

    # --- Invalidation Conditions ---
    invalidation = []
    if sma_50:
        if direction in ("bullish", "strong_bullish"):
            invalidation.append({"condition": f"Price drops below 50-day SMA ({sma_50:.2f})", "type": "price"})
        else:
            invalidation.append({"condition": f"Price breaks above 50-day SMA ({sma_50:.2f})", "type": "price"})
    invalidation.append({"condition": "Significant unexpected news event changes fundamentals", "type": "event"})

    return {
        "symbol": symbol,
        "asset_type": asset_type,
        "direction": direction,
        "final_score": round(final_score, 2),
        "confidence_score": round(confidence, 1),
        "risk_level": risk_result["risk_level"],
        "time_horizon": time_horizon,
        "price_at_signal": price,
        "expected_move_low": expected_range["low"],
        "expected_move_high": expected_range["high"],

        # Component scores (transparency)
        "technical_score": round(technical_score, 2),
        "fundamental_score": round(fundamental_score, 2),
        "news_score": round(news_score, 2),
        "market_context_score": round(market_context_score, 2),
        "onchain_score": round(onchain_score, 2) if asset_type == "crypto" else None,
        "data_quality_score": round(data_quality, 2),
        "risk_penalty": round(risk_penalty, 2),

        # Evidence
        "bull_factors": bull_factors[:3],
        "bear_factors": bear_factors[:3],
        "key_risks": key_risks[:3],
        "invalidation_conditions": invalidation,
        "conflicting_signals": [
            {"indicator": "bull" if bf else "none", "counter": "bear" if bf else "none"}
            for bf in (bull_factors[:1] if bear_factors else [])
        ] if bull_factors and bear_factors else None,

        # Metadata
        "weights_used": STOCK_WEIGHTS if asset_type == "stock" else CRYPTO_WEIGHTS,
        "data_sources": ["demo_mock"],
        "calculation_timestamp": now.isoformat(),
        "expires_at": (now + timedelta(hours=24)).isoformat(),
        "config_version": "v0.1.0",
        "model_version": "rule_based_v1",
        "disclaimer": SIGNAL_DISCLAIMER,

        # Technical detail
        "indicators": indicators,
        "feature_contributions": tech_result.get("sub_scores", {}),
    }
