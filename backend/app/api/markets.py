"""
MarketPulse AI — Market Data API Routes
GET /markets/overview, /markets/movers, /markets/breadth
GET /assets, /assets/{symbol}, /assets/{symbol}/candles, /assets/{symbol}/indicators, /assets/{symbol}/fundamentals, /assets/{symbol}/onchain
"""
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import get_settings
from app.providers.mock_provider import (
    MockMarketDataProvider, MockFundamentalProvider, MockOnchainProvider,
    MOCK_STOCKS, MOCK_CRYPTO, MOCK_INDICES,
)
from app.analytics.technical import compute_all_indicators
from app.analytics.signal_engine import generate_signal_for_asset, SIGNAL_DISCLAIMER

settings = get_settings()
router = APIRouter(prefix="/api", tags=["Market Data"])


def get_market_provider():
    """Get the appropriate market data provider based on mode."""
    # In demo mode, always use mock. In production, would check API keys.
    return MockMarketDataProvider("stock"), MockMarketDataProvider("crypto")


@router.get("/markets/overview")
async def market_overview():
    """Get global market overview including indices, crypto, and market regime."""
    stock_provider, crypto_provider = get_market_provider()

    stock_overview = await stock_provider.get_market_overview()
    crypto_overview = await crypto_provider.get_market_overview()

    # Build overview response
    now = datetime.now(timezone.utc)

    # Get movers
    stock_movers = await stock_provider.get_movers()
    crypto_movers = await crypto_provider.get_movers()

    return {
        "timestamp": now.isoformat(),
        "demo_mode": settings.DEMO_MODE,
        "global_market": {
            "indices": stock_overview.get("indices", []),
            "market_regime": stock_overview.get("market_regime", "sideways"),
            "risk_condition": stock_overview.get("risk_condition", "neutral"),
        },
        "us_market": {
            "indices": [i for i in stock_overview.get("indices", []) if i.get("country") == "United States"],
            "last_updated": now.isoformat(),
        },
        "id_market": {
            "indices": [i for i in stock_overview.get("indices", []) if i.get("country") == "Indonesia"],
            "last_updated": now.isoformat(),
        },
        "crypto_market": {
            "total_market_cap": crypto_overview.get("crypto_total_market_cap"),
            "btc_dominance": crypto_overview.get("btc_dominance"),
            "eth_dominance": crypto_overview.get("eth_dominance"),
            "fear_greed_index": crypto_overview.get("fear_greed_index"),
            "fear_greed_label": crypto_overview.get("fear_greed_label"),
            "last_updated": now.isoformat(),
        },
        "top_gainers": (stock_movers.get("gainers", []) + crypto_movers.get("gainers", []))[:10],
        "top_losers": (stock_movers.get("losers", []) + crypto_movers.get("losers", []))[:10],
        "most_active": stock_movers.get("most_active", [])[:5],
        "unusual_volume": stock_movers.get("unusual_volume", [])[:5],
        "high_impact_news": [],  # Will be populated by news endpoint
        "market_regime": stock_overview.get("market_regime", "sideways"),
        "risk_condition": stock_overview.get("risk_condition", "neutral"),
        "disclaimer": SIGNAL_DISCLAIMER,
        "data_freshness": "demo" if settings.DEMO_MODE else "delayed",
    }


@router.get("/markets/movers")
async def market_movers(
    asset_type: str = Query("all", enum=["stock", "crypto", "all"]),
):
    """Get top gainers, losers, most active, unusual volume."""
    stock_provider, crypto_provider = get_market_provider()
    now = datetime.now(timezone.utc)

    result = {"gainers": [], "losers": [], "most_active": [], "unusual_volume": [], "timestamp": now.isoformat(), "demo_mode": settings.DEMO_MODE}

    if asset_type in ("stock", "all"):
        stock_movers = await stock_provider.get_movers()
        result["gainers"].extend(stock_movers.get("gainers", []))
        result["losers"].extend(stock_movers.get("losers", []))
        result["most_active"].extend(stock_movers.get("most_active", []))
        result["unusual_volume"].extend(stock_movers.get("unusual_volume", []))

    if asset_type in ("crypto", "all"):
        crypto_movers = await crypto_provider.get_movers()
        result["gainers"].extend(crypto_movers.get("gainers", []))
        result["losers"].extend(crypto_movers.get("losers", []))
        result["most_active"].extend(crypto_movers.get("most_active", []))

    # Sort combined
    result["gainers"] = sorted(result["gainers"], key=lambda x: x.get("change_pct", 0), reverse=True)[:10]
    result["losers"] = sorted(result["losers"], key=lambda x: x.get("change_pct", 0))[:10]

    return result


@router.get("/assets")
async def list_assets(
    asset_type: Optional[str] = Query(None, enum=["stock", "crypto"]),
    country: Optional[str] = None,
    sector: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("name", enum=["name", "symbol", "market_cap", "price", "change_pct"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List and filter assets with pagination."""
    all_assets = []

    if asset_type != "crypto":
        for s in MOCK_STOCKS:
            all_assets.append({**s, "asset_type": "stock"})

    if asset_type != "stock":
        for c in MOCK_CRYPTO:
            all_assets.append({**c, "asset_type": "crypto"})

    # Apply filters
    if country:
        all_assets = [a for a in all_assets if a.get("country", "").lower() == country.lower()]
    if sector:
        all_assets = [a for a in all_assets if a.get("sector", "").lower() == sector.lower()]
    if search:
        search_lower = search.lower()
        all_assets = [a for a in all_assets if search_lower in a["symbol"].lower() or search_lower in a["name"].lower()]

    # Add price change for sorting
    import random
    for a in all_assets:
        a["change_pct"] = round(random.uniform(-5, 6), 2)

    # Sort
    reverse = sort_order == "desc"
    try:
        all_assets.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)
    except TypeError:
        pass

    # Paginate
    total = len(all_assets)
    start = (page - 1) * page_size
    end = start + page_size
    items = all_assets[start:end]

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "demo_mode": settings.DEMO_MODE,
    }


@router.get("/assets/{symbol}")
async def get_asset(symbol: str):
    """Get detailed asset information."""
    stock_provider, crypto_provider = get_market_provider()

    # Find the asset
    all_assets = MOCK_STOCKS + MOCK_CRYPTO
    asset_data = next((a for a in all_assets if a["symbol"] == symbol), None)
    if not asset_data:
        raise HTTPException(status_code=404, detail=f"Asset {symbol} not found")

    asset_type = "crypto" if asset_data in MOCK_CRYPTO else "stock"
    provider = crypto_provider if asset_type == "crypto" else stock_provider

    # Get price data
    price_data = await provider.get_price(symbol)

    # Get candles for chart
    candles = await provider.get_candles(symbol, interval="1d", limit=90)

    # Compute technical indicators
    indicators = compute_all_indicators(candles) if candles else {}

    # Get fundamentals (stocks only)
    fundamental_data = None
    if asset_type == "stock":
        fund_provider = MockFundamentalProvider()
        fundamental_data = await fund_provider.get_fundamentals(symbol)

    # Get on-chain (crypto only)
    onchain_data = None
    if asset_type == "crypto":
        onchain_provider = MockOnchainProvider()
        onchain_data = await onchain_provider.get_onchain_metrics(symbol)

    # Get news
    from app.providers.mock_provider import MockNewsProvider
    news_provider = MockNewsProvider()
    related_news = await news_provider.get_news_for_asset(symbol)

    # Generate signal
    signal = generate_signal_for_asset(
        symbol=symbol,
        asset_type=asset_type,
        candles=candles,
        news_data=related_news,
        fundamental_data=fundamental_data,
        onchain_data=onchain_data,
    )

    return {
        "asset": {
            **asset_data,
            "asset_type": asset_type,
            "data_quality_score": 75 if settings.DEMO_MODE else None,
            "liquidity_tier": "high",
            "manipulation_risk": False,
            "low_liquidity_warning": False,
            "unverified_contract": False,
            "has_sufficient_history": True,
        },
        "price": price_data,
        "indicators": indicators,
        "fundamentals": fundamental_data,
        "onchain": onchain_data,
        "news": related_news[:5],
        "signal": signal if not signal.get("error") else None,
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/assets/{symbol}/candles")
async def get_candles(
    symbol: str,
    interval: str = Query("1d", enum=["1h", "4h", "1d", "1w"]),
    limit: int = Query(90, ge=1, le=365),
):
    """Get OHLCV candlestick data for charting."""
    stock_provider, crypto_provider = get_market_provider()
    all_assets = MOCK_STOCKS + MOCK_CRYPTO
    asset_data = next((a for a in all_assets if a["symbol"] == symbol), None)
    if not asset_data:
        raise HTTPException(status_code=404, detail=f"Asset {symbol} not found")

    provider = crypto_provider if asset_data in MOCK_CRYPTO else stock_provider
    candles = await provider.get_candles(symbol, interval=interval, limit=limit)

    return {
        "symbol": symbol,
        "interval": interval,
        "candles": candles,
        "count": len(candles),
        "demo_mode": settings.DEMO_MODE,
        "data_freshness": "demo" if settings.DEMO_MODE else "delayed",
    }


@router.get("/assets/{symbol}/indicators")
async def get_indicators(
    symbol: str,
    interval: str = Query("1d", enum=["1h", "4h", "1d", "1w"]),
):
    """Get computed technical indicators."""
    stock_provider, crypto_provider = get_market_provider()
    all_assets = MOCK_STOCKS + MOCK_CRYPTO
    asset_data = next((a for a in all_assets if a["symbol"] == symbol), None)
    if not asset_data:
        raise HTTPException(status_code=404, detail=f"Asset {symbol} not found")

    provider = crypto_provider if asset_data in MOCK_CRYPTO else stock_provider
    candles = await provider.get_candles(symbol, interval=interval, limit=200)
    indicators = compute_all_indicators(candles, interval) if candles else {}

    return {
        "symbol": symbol,
        "interval": interval,
        "indicators": indicators,
        "demo_mode": settings.DEMO_MODE,
    }


@router.get("/assets/{symbol}/fundamentals")
async def get_fundamentals(symbol: str):
    """Get fundamental data for a stock."""
    asset_data = next((a for a in MOCK_STOCKS if a["symbol"] == symbol), None)
    if not asset_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found or fundamentals not available")

    provider = MockFundamentalProvider()
    data = await provider.get_fundamentals(symbol)
    return {"symbol": symbol, "fundamentals": data, "demo_mode": settings.DEMO_MODE}


@router.get("/assets/{symbol}/onchain")
async def get_onchain(symbol: str):
    """Get on-chain metrics for a cryptocurrency."""
    asset_data = next((a for a in MOCK_CRYPTO if a["symbol"] == symbol), None)
    if not asset_data:
        raise HTTPException(status_code=404, detail=f"Crypto {symbol} not found or on-chain data not available")

    provider = MockOnchainProvider()
    data = await provider.get_onchain_metrics(symbol)
    return {"symbol": symbol, "onchain": data, "demo_mode": settings.DEMO_MODE}
