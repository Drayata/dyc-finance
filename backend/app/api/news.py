"""
MarketPulse AI — News Intelligence API Routes
GET /news, /news/{id}, /news/high-impact, /assets/{symbol}/news
"""
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from app.config import get_settings
from app.providers.mock_provider import MockNewsProvider, MOCK_NEWS

settings = get_settings()
router = APIRouter(prefix="/api/news", tags=["News Intelligence"])


@router.get("")
async def list_news(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    event_category: Optional[str] = None,
    impact_direction: Optional[str] = None,
    min_impact_score: Optional[float] = None,
    is_verified: Optional[bool] = None,
):
    """List news articles with filtering."""
    provider = MockNewsProvider()
    news = await provider.get_latest_news(limit=100)

    # Apply filters
    if event_category:
        news = [n for n in news if n.get("event_category") == event_category]
    if impact_direction:
        news = [n for n in news if n.get("impact_direction") == impact_direction]
    if min_impact_score is not None:
        news = [n for n in news if (n.get("impact_score") or 0) >= min_impact_score]
    if is_verified is not None:
        news = [n for n in news if n.get("is_verified") == is_verified]

    # Add unique IDs to each article for the frontend
    for i, article in enumerate(news):
        article["id"] = str(uuid4())

    total = len(news)
    items = news[offset:offset + limit]

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/high-impact")
async def high_impact_news(limit: int = Query(10, ge=1, le=50)):
    """Get highest-impact news articles."""
    provider = MockNewsProvider()
    news = await provider.get_high_impact_news(limit=limit)

    for i, article in enumerate(news):
        article["id"] = str(uuid4())

    return {
        "items": news,
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/categories")
async def news_categories():
    """Get available event categories."""
    categories = [
        {"value": "earnings", "label": "Earnings"},
        {"value": "revenue_guidance", "label": "Revenue Guidance"},
        {"value": "dividend", "label": "Dividend"},
        {"value": "merger_acquisition", "label": "Merger & Acquisition"},
        {"value": "regulatory_action", "label": "Regulatory Action"},
        {"value": "monetary_policy", "label": "Monetary Policy"},
        {"value": "interest_rate", "label": "Interest Rate"},
        {"value": "inflation_data", "label": "Inflation Data"},
        {"value": "geopolitical_conflict", "label": "Geopolitical Conflict"},
        {"value": "exchange_listing", "label": "Exchange Listing"},
        {"value": "token_unlock", "label": "Token Unlock"},
        {"value": "protocol_upgrade", "label": "Protocol Upgrade"},
        {"value": "security_exploit", "label": "Security Exploit"},
        {"value": "etf_flow", "label": "ETF Flow"},
        {"value": "strategic_partnership", "label": "Strategic Partnership"},
        {"value": "rumor", "label": "Rumor"},
    ]
    return {"categories": categories}


@router.get("/asset/{symbol}")
async def news_for_asset(symbol: str, limit: int = Query(20, ge=1, le=50)):
    """Get news related to a specific asset."""
    provider = MockNewsProvider()
    news = await provider.get_news_for_asset(symbol, limit=limit)

    for article in news:
        article["id"] = str(uuid4())

    return {
        "symbol": symbol,
        "items": news,
        "total": len(news),
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
