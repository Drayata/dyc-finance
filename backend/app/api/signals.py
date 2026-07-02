"""
MarketPulse AI — Signal & Recommendation API Routes
GET /signals, /signals/{id}, /assets/{symbol}/signal, /assets/{symbol}/signal-history
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from app.config import get_settings
from app.providers.mock_provider import (
    MockMarketDataProvider, MockNewsProvider,
    MockFundamentalProvider, MockOnchainProvider,
    MOCK_STOCKS, MOCK_CRYPTO,
)
from app.analytics.signal_engine import generate_signal_for_asset, SIGNAL_DISCLAIMER

settings = get_settings()
router = APIRouter(prefix="/api/signals", tags=["Signals"])


@router.get("")
async def list_signals(
    asset_type: Optional[str] = Query(None, enum=["stock", "crypto"]),
    direction: Optional[str] = Query(None, enum=["strong_bullish", "bullish", "neutral", "bearish", "strong_bearish"]),
    min_confidence: Optional[float] = Query(None, ge=0, le=100),
    sort_by: str = Query("confidence_score", enum=["confidence_score", "final_score", "risk_level"]),
    sort_order: str = Query("desc", enum=["asc", "desc"]),
    limit: int = Query(20, ge=1, le=100),
):
    """Get all current signals with filtering."""
    stock_provider = MockMarketDataProvider("stock")
    crypto_provider = MockMarketDataProvider("crypto")
    news_provider = MockNewsProvider()
    fund_provider = MockFundamentalProvider()
    onchain_provider = MockOnchainProvider()

    all_assets = []
    if asset_type != "crypto":
        all_assets.extend([(s, "stock") for s in MOCK_STOCKS])
    if asset_type != "stock":
        all_assets.extend([(c, "crypto") for c in MOCK_CRYPTO])

    # Filter out stablecoins from signals
    all_assets = [(a, t) for a, t in all_assets if a["symbol"] not in ("USDT", "USDC")]

    signals = []
    for asset_data, a_type in all_assets:
        provider = crypto_provider if a_type == "crypto" else stock_provider
        candles = await provider.get_candles(asset_data["symbol"], interval="1d", limit=90)

        related_news = await news_provider.get_news_for_asset(asset_data["symbol"])

        fundamental_data = None
        onchain_data = None
        if a_type == "stock":
            fundamental_data = await fund_provider.get_fundamentals(asset_data["symbol"])
        else:
            onchain_data = await onchain_provider.get_onchain_metrics(asset_data["symbol"])

        signal = generate_signal_for_asset(
            symbol=asset_data["symbol"],
            asset_type=a_type,
            candles=candles,
            news_data=related_news,
            fundamental_data=fundamental_data,
            onchain_data=onchain_data,
        )

        if signal and not signal.get("error"):
            signal["asset_name"] = asset_data["name"]
            signals.append(signal)

    # Apply filters
    if direction:
        signals = [s for s in signals if s.get("direction") == direction]
    if min_confidence is not None:
        signals = [s for s in signals if (s.get("confidence_score") or 0) >= min_confidence]

    # Sort
    reverse = sort_order == "desc"
    signals.sort(key=lambda x: abs(x.get(sort_by, 0)) if isinstance(x.get(sort_by, 0), (int, float)) else 0, reverse=reverse)

    return {
        "items": signals[:limit],
        "total": len(signals),
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "disclaimer": SIGNAL_DISCLAIMER,
    }


@router.get("/strongest-bullish")
async def strongest_bullish(limit: int = Query(5, ge=1, le=20)):
    """Get assets with the strongest bullish signals."""
    result = await list_signals(direction="strong_bullish", sort_by="final_score", sort_order="desc", limit=limit)
    if len(result["items"]) < limit:
        bullish = await list_signals(direction="bullish", sort_by="final_score", sort_order="desc", limit=limit)
        result["items"].extend(bullish["items"])
    result["items"] = result["items"][:limit]
    return result


@router.get("/strongest-bearish")
async def strongest_bearish(limit: int = Query(5, ge=1, le=20)):
    """Get assets with the strongest bearish signals."""
    result = await list_signals(direction="strong_bearish", sort_by="final_score", sort_order="asc", limit=limit)
    if len(result["items"]) < limit:
        bearish = await list_signals(direction="bearish", sort_by="final_score", sort_order="asc", limit=limit)
        result["items"].extend(bearish["items"])
    result["items"] = result["items"][:limit]
    return result


@router.get("/asset/{symbol}")
async def get_asset_signal(symbol: str):
    """Get the current signal for a specific asset."""
    all_assets = MOCK_STOCKS + MOCK_CRYPTO
    asset_data = next((a for a in all_assets if a["symbol"] == symbol), None)
    if not asset_data:
        return {"error": f"Asset {symbol} not found", "demo_mode": settings.DEMO_MODE}

    asset_type = "crypto" if asset_data in MOCK_CRYPTO else "stock"
    provider = MockMarketDataProvider(asset_type)
    news_provider = MockNewsProvider()

    candles = await provider.get_candles(symbol, interval="1d", limit=90)
    related_news = await news_provider.get_news_for_asset(symbol)

    fundamental_data = None
    onchain_data = None
    if asset_type == "stock":
        fundamental_data = await MockFundamentalProvider().get_fundamentals(symbol)
    else:
        onchain_data = await MockOnchainProvider().get_onchain_metrics(symbol)

    signal = generate_signal_for_asset(
        symbol=symbol,
        asset_type=asset_type,
        candles=candles,
        news_data=related_news,
        fundamental_data=fundamental_data,
        onchain_data=onchain_data,
    )

    signal["asset_name"] = asset_data["name"]

    return {
        "signal": signal,
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
