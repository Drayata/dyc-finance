"""
MarketPulse AI — Mock Data Provider (Demo Mode)
Generates realistic but clearly labeled mock data for the entire platform.
All data is marked with provider="demo_mock" and data_freshness="demo".
"""
import random
import math
import hashlib
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from app.providers.base import MarketDataProvider, NewsProvider, FundamentalProvider, OnchainProvider


# ==============================================================================
# Mock Asset Data
# ==============================================================================

MOCK_STOCKS = [
    {"symbol": "BBCA.JK", "name": "Bank Central Asia", "sector": "Financial Services", "industry": "Banks", "country": "Indonesia", "currency": "IDR", "price": 9850, "market_cap": 1210000000000000},
    {"symbol": "BBRI.JK", "name": "Bank Rakyat Indonesia", "sector": "Financial Services", "industry": "Banks", "country": "Indonesia", "currency": "IDR", "price": 5625, "market_cap": 850000000000000},
    {"symbol": "TLKM.JK", "name": "Telkom Indonesia", "sector": "Communication Services", "industry": "Telecom", "country": "Indonesia", "currency": "IDR", "price": 3850, "market_cap": 380000000000000},
    {"symbol": "ASII.JK", "name": "Astra International", "sector": "Industrials", "industry": "Diversified", "country": "Indonesia", "currency": "IDR", "price": 5225, "market_cap": 210000000000000},
    {"symbol": "BMRI.JK", "name": "Bank Mandiri", "sector": "Financial Services", "industry": "Banks", "country": "Indonesia", "currency": "IDR", "price": 6500, "market_cap": 300000000000000},
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "country": "United States", "currency": "USD", "price": 195.50, "market_cap": 3050000000000},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "industry": "Software", "country": "United States", "currency": "USD", "price": 425.20, "market_cap": 3160000000000},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "industry": "Internet Services", "country": "United States", "currency": "USD", "price": 178.30, "market_cap": 2200000000000},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "industry": "E-Commerce", "country": "United States", "currency": "USD", "price": 198.40, "market_cap": 2050000000000},
    {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors", "country": "United States", "currency": "USD", "price": 135.60, "market_cap": 3340000000000},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Discretionary", "industry": "Auto Manufacturers", "country": "United States", "currency": "USD", "price": 248.90, "market_cap": 790000000000},
    {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Technology", "industry": "Internet Services", "country": "United States", "currency": "USD", "price": 510.70, "market_cap": 1300000000000},
]

MOCK_CRYPTO = [
    {"symbol": "BTC", "name": "Bitcoin", "currency": "USD", "price": 67450.00, "market_cap": 1325000000000, "circulating_supply": 19650000, "max_supply": 21000000},
    {"symbol": "ETH", "name": "Ethereum", "currency": "USD", "price": 3520.00, "market_cap": 423000000000, "circulating_supply": 120200000, "max_supply": None},
    {"symbol": "BNB", "name": "BNB", "currency": "USD", "price": 605.00, "market_cap": 93000000000, "circulating_supply": 153900000, "max_supply": 200000000},
    {"symbol": "SOL", "name": "Solana", "currency": "USD", "price": 172.30, "market_cap": 78500000000, "circulating_supply": 455000000, "max_supply": None},
    {"symbol": "XRP", "name": "XRP", "currency": "USD", "price": 0.62, "market_cap": 34000000000, "circulating_supply": 54800000000, "max_supply": 100000000000},
    {"symbol": "ADA", "name": "Cardano", "currency": "USD", "price": 0.45, "market_cap": 16000000000, "circulating_supply": 35500000000, "max_supply": 45000000000},
    {"symbol": "DOGE", "name": "Dogecoin", "currency": "USD", "price": 0.135, "market_cap": 19300000000, "circulating_supply": 143000000000, "max_supply": None},
    {"symbol": "USDT", "name": "Tether", "currency": "USD", "price": 1.00, "market_cap": 112000000000, "circulating_supply": 112000000000, "max_supply": None},
    {"symbol": "USDC", "name": "USD Coin", "currency": "USD", "price": 1.00, "market_cap": 33500000000, "circulating_supply": 33500000000, "max_supply": None},
]

MOCK_INDICES = [
    {"symbol": "^JKSE", "name": "Jakarta Composite Index (IHSG)", "country": "Indonesia", "price": 7285.50, "change_pct": 0.45},
    {"symbol": "^GSPC", "name": "S&P 500", "country": "United States", "price": 5475.20, "change_pct": 0.32},
    {"symbol": "^IXIC", "name": "NASDAQ Composite", "country": "United States", "price": 17250.80, "change_pct": 0.68},
    {"symbol": "^DJI", "name": "Dow Jones Industrial Average", "country": "United States", "price": 39280.40, "change_pct": 0.15},
]


def _generate_seed(symbol: str, date: str = None) -> int:
    """Deterministic seed for consistent demo data."""
    seed_str = f"{symbol}_{date or datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    return int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)


def _jitter(value: float, pct: float = 0.03) -> float:
    """Add small deterministic jitter to a value."""
    return value * (1 + random.uniform(-pct, pct))


def _generate_candles(base_price: float, days: int = 90, interval: str = "1d") -> List[Dict[str, Any]]:
    """Generate realistic OHLCV candles with trend and volatility."""
    candles = []
    price = base_price * 0.85  # Start lower to show trend
    now = datetime.now(timezone.utc)

    # Determine number of periods
    if interval == "1d":
        num_periods = days
        delta = timedelta(days=1)
    elif interval == "1h":
        num_periods = min(days * 24, 720)
        delta = timedelta(hours=1)
    elif interval == "4h":
        num_periods = min(days * 6, 360)
        delta = timedelta(hours=4)
    elif interval == "1w":
        num_periods = days // 7
        delta = timedelta(weeks=1)
    else:
        num_periods = days
        delta = timedelta(days=1)

    volatility = 0.02 if base_price > 100 else 0.035
    trend = 0.001  # Slight upward drift

    for i in range(num_periods):
        ts = now - delta * (num_periods - i)
        change = random.gauss(trend, volatility)
        price = price * (1 + change)

        open_price = price * (1 + random.gauss(0, 0.005))
        high_price = max(price, open_price) * (1 + abs(random.gauss(0, 0.01)))
        low_price = min(price, open_price) * (1 - abs(random.gauss(0, 0.01)))
        close_price = price
        volume = random.randint(1000000, 50000000) * (1 + abs(random.gauss(0, 0.5)))

        candles.append({
            "timestamp": ts.isoformat(),
            "open": round(open_price, 8),
            "high": round(high_price, 8),
            "low": round(low_price, 8),
            "close": round(close_price, 8),
            "volume": round(volume),
        })

    return candles


# ==============================================================================
# Mock News Data
# ==============================================================================

MOCK_NEWS = [
    {
        "title": "Bank Indonesia Holds Interest Rate Steady at 6.25%, Signals Cautious Outlook",
        "summary": "Bank Indonesia maintained its benchmark interest rate at 6.25% amid stable inflation and a weakening rupiah. The central bank signaled a data-dependent approach for future decisions.",
        "source_name": "Demo Financial News",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        "event_category": "interest_rate",
        "impact_score": 78,
        "impact_direction": "mixed",
        "impact_time_horizon": "short_term",
        "relevance_score": 85,
        "overall_sentiment": -0.1,
        "is_verified": True,
        "related_assets": ["BBCA.JK", "BBRI.JK", "BMRI.JK", "^JKSE"],
        "impact_pathway": "Interest rate hold → stable borrowing costs → neutral for bank lending margins → supports financial sector stability → possible rupiah weakness if rate cut expectations diminish",
        "source_credibility_score": 95,
    },
    {
        "title": "Bitcoin ETF Sees Record $1.2B Net Inflows Amid Institutional Accumulation",
        "summary": "US-listed Bitcoin spot ETFs recorded their highest single-day net inflow of $1.2 billion, driven by institutional allocators increasing crypto exposure ahead of the anticipated halving supply effect.",
        "source_name": "Demo Crypto News",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=4)).isoformat(),
        "event_category": "etf_flow",
        "impact_score": 82,
        "impact_direction": "bullish",
        "impact_time_horizon": "short_term",
        "relevance_score": 90,
        "overall_sentiment": 0.65,
        "is_verified": True,
        "related_assets": ["BTC", "ETH"],
        "impact_pathway": "Record ETF inflows → increased institutional demand → reduced available supply on exchanges → potential upward price pressure → may trigger momentum-driven buying",
        "source_credibility_score": 88,
    },
    {
        "title": "NVIDIA Reports Q3 Revenue of $35.1B, Beating Estimates by 8%",
        "summary": "NVIDIA reported quarterly revenue of $35.1 billion, surpassing analyst estimates of $32.5 billion. Data center segment grew 112% YoY, driven by AI chip demand. The company raised Q4 guidance above consensus.",
        "source_name": "Demo Market Wire",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat(),
        "event_category": "earnings",
        "impact_score": 88,
        "impact_direction": "bullish",
        "impact_time_horizon": "short_term",
        "relevance_score": 95,
        "overall_sentiment": 0.78,
        "is_verified": True,
        "related_assets": ["NVDA", "MSFT", "GOOGL", "AMZN"],
        "impact_pathway": "Earnings beat + raised guidance → validates AI spending thesis → positive for semiconductor sector → may drive broader tech sentiment → increased revenue visibility",
        "source_credibility_score": 92,
    },
    {
        "title": "Ethereum Protocol Upgrade 'Pectra' Activates Successfully on Mainnet",
        "summary": "Ethereum's Pectra upgrade went live on mainnet without issues, introducing account abstraction improvements and validator efficiency changes. Gas costs for certain operations reduced by an estimated 30%.",
        "source_name": "Demo Blockchain News",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat(),
        "event_category": "protocol_upgrade",
        "impact_score": 72,
        "impact_direction": "bullish",
        "impact_time_horizon": "medium_term",
        "relevance_score": 88,
        "overall_sentiment": 0.55,
        "is_verified": True,
        "related_assets": ["ETH", "SOL"],
        "impact_pathway": "Successful upgrade → improved user experience → lower transaction costs → potential increase in network usage → positive for ETH value accrual",
        "source_credibility_score": 85,
    },
    {
        "title": "Indonesia's OJK Announces New Crypto Exchange Regulations Effective Q1 2025",
        "summary": "Indonesia's Financial Services Authority (OJK) released draft regulations for cryptocurrency exchanges operating in Indonesia, requiring increased capital reserves and user protection measures.",
        "source_name": "Demo Regulatory Watch",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat(),
        "event_category": "regulatory_action",
        "impact_score": 65,
        "impact_direction": "mixed",
        "impact_time_horizon": "medium_term",
        "relevance_score": 70,
        "overall_sentiment": 0.1,
        "is_verified": True,
        "related_assets": ["BTC", "ETH", "^JKSE"],
        "impact_pathway": "New regulations → increased compliance costs for exchanges → may reduce smaller operators → improved investor protection → potential for greater institutional participation long-term",
        "source_credibility_score": 90,
    },
    {
        "title": "Major Solana Token Unlock: 15M SOL to Enter Circulation in 7 Days",
        "summary": "Approximately 15 million SOL tokens (worth ~$2.6B) are scheduled to unlock from staking contracts in the next 7 days. This represents approximately 3.3% of the current circulating supply.",
        "source_name": "Demo On-Chain Analytics",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=14)).isoformat(),
        "event_category": "token_unlock",
        "impact_score": 70,
        "impact_direction": "bearish",
        "impact_time_horizon": "short_term",
        "relevance_score": 85,
        "overall_sentiment": -0.35,
        "is_verified": True,
        "related_assets": ["SOL"],
        "impact_pathway": "Large token unlock → increased circulating supply → higher potential selling pressure → may create short-term downside risk → historical unlocks have seen 5-15% price impact",
        "source_credibility_score": 82,
    },
    {
        "title": "Apple Announces AI Partnership with OpenAI for iPhone 17 Features",
        "summary": "Apple confirmed a multi-year partnership with OpenAI to integrate advanced AI capabilities into the upcoming iPhone 17 line, including on-device language models and enhanced Siri functionality.",
        "source_name": "Demo Tech News",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=18)).isoformat(),
        "event_category": "strategic_partnership",
        "impact_score": 75,
        "impact_direction": "bullish",
        "impact_time_horizon": "medium_term",
        "relevance_score": 82,
        "overall_sentiment": 0.62,
        "is_verified": True,
        "related_assets": ["AAPL", "MSFT", "NVDA"],
        "impact_pathway": "AI partnership → competitive iPhone features → potential upgrade cycle boost → increased services revenue opportunity → positive for Apple ecosystem valuation",
        "source_credibility_score": 88,
    },
    {
        "title": "UNVERIFIED: Rumored Acquisition of Major Indonesian Fintech by Regional Bank",
        "summary": "Unconfirmed reports suggest a major Indonesian bank may be in advanced talks to acquire a leading fintech company. Neither party has issued an official statement.",
        "source_name": "Demo Social Feed",
        "published_at": (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat(),
        "event_category": "rumor",
        "impact_score": 40,
        "impact_direction": "uncertain",
        "impact_time_horizon": "short_term",
        "relevance_score": 55,
        "overall_sentiment": 0.2,
        "is_verified": False,
        "related_assets": ["BBCA.JK", "BBRI.JK"],
        "impact_pathway": "Unverified rumor → uncertain impact → requires official confirmation → if true, may signal fintech consolidation → potential M&A premium for target",
        "source_credibility_score": 30,
    },
]


# ==============================================================================
# Mock Provider Implementations
# ==============================================================================

class MockMarketDataProvider(MarketDataProvider):
    """Mock market data provider for demo mode. All data clearly labeled as demo."""

    def __init__(self, asset_type: str = "stock"):
        self.asset_type = asset_type
        self._assets = MOCK_STOCKS if asset_type == "stock" else MOCK_CRYPTO

    async def get_price(self, symbol: str) -> Dict[str, Any]:
        asset = next((a for a in self._assets if a["symbol"] == symbol), None)
        if not asset:
            # Also check other lists
            asset = next((a for a in MOCK_STOCKS + MOCK_CRYPTO if a["symbol"] == symbol), None)
        if not asset:
            return {}

        price = _jitter(asset["price"])
        change_pct = random.uniform(-3, 4)
        change = price * change_pct / 100

        return {
            "symbol": asset["symbol"],
            "name": asset["name"],
            "price": round(price, 8),
            "price_change_24h": round(change, 8),
            "price_change_pct_24h": round(change_pct, 2),
            "volume_24h": round(random.uniform(10000000, 500000000), 2),
            "market_cap": asset.get("market_cap", 0),
            "high_24h": round(price * 1.02, 8),
            "low_24h": round(price * 0.98, 8),
            "open_24h": round(price * (1 - change_pct / 100), 8),
            "currency": asset.get("currency", "USD"),
            "provider": "demo_mock",
            "data_timestamp": datetime.now(timezone.utc).isoformat(),
            "data_freshness": "demo",
            "data_status": "demo",
        }

    async def get_candles(self, symbol: str, interval: str = "1d", limit: int = 90) -> List[Dict[str, Any]]:
        asset = next((a for a in MOCK_STOCKS + MOCK_CRYPTO if a["symbol"] == symbol), None)
        if not asset:
            return []

        random.seed(_generate_seed(symbol))
        candles = _generate_candles(asset["price"], days=limit, interval=interval)
        random.seed()  # Reset
        return candles

    async def get_market_overview(self) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)

        # Generate overview for each market
        indices_data = []
        for idx in MOCK_INDICES:
            change_pct = _jitter(idx["change_pct"], 0.5)
            indices_data.append({
                "symbol": idx["symbol"],
                "name": idx["name"],
                "price": round(_jitter(idx["price"]), 2),
                "change_pct": round(change_pct, 2),
                "country": idx["country"],
            })

        return {
            "timestamp": now.isoformat(),
            "demo_mode": True,
            "indices": indices_data,
            "market_regime": "sideways",
            "risk_condition": "risk_on",
            "crypto_total_market_cap": 2650000000000,
            "btc_dominance": 52.4,
            "eth_dominance": 16.8,
            "fear_greed_index": 62,
            "fear_greed_label": "Greed",
            "provider": "demo_mock",
            "data_freshness": "demo",
        }

    async def get_movers(self) -> Dict[str, Any]:
        all_assets = self._assets.copy()
        movers = []
        for a in all_assets:
            change = random.uniform(-8, 10)
            movers.append({
                "symbol": a["symbol"],
                "name": a["name"],
                "price": round(_jitter(a["price"]), 8),
                "change_pct": round(change, 2),
                "volume": round(random.uniform(5000000, 200000000), 2),
                "relative_volume": round(random.uniform(0.5, 3.5), 2),
            })

        sorted_by_change = sorted(movers, key=lambda x: x["change_pct"], reverse=True)
        sorted_by_volume = sorted(movers, key=lambda x: x["volume"], reverse=True)

        return {
            "gainers": sorted_by_change[:5],
            "losers": sorted_by_change[-5:][::-1],
            "most_active": sorted_by_volume[:5],
            "unusual_volume": [m for m in movers if m["relative_volume"] > 2.0][:5],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "demo_mode": True,
        }

    async def search(self, query: str) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        results = []
        for a in MOCK_STOCKS + MOCK_CRYPTO:
            if query_lower in a["symbol"].lower() or query_lower in a["name"].lower():
                results.append({
                    "symbol": a["symbol"],
                    "name": a["name"],
                    "asset_type": "crypto" if a in MOCK_CRYPTO else "stock",
                })
        return results

    def get_provider_name(self) -> str:
        return "demo_mock"

    def get_data_freshness(self) -> str:
        return "demo"


class MockNewsProvider(NewsProvider):
    """Mock news provider for demo mode."""

    async def get_latest_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        return MOCK_NEWS[:limit]

    async def get_news_for_asset(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        return [
            n for n in MOCK_NEWS
            if symbol in n.get("related_assets", [])
        ][:limit]

    async def get_high_impact_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        return sorted(MOCK_NEWS, key=lambda x: x.get("impact_score", 0), reverse=True)[:limit]

    def get_provider_name(self) -> str:
        return "demo_mock"


class MockFundamentalProvider(FundamentalProvider):
    """Mock fundamental data provider for demo mode."""

    async def get_fundamentals(self, symbol: str) -> Dict[str, Any]:
        return {
            "symbol": symbol,
            "period": "TTM",
            "revenue": round(random.uniform(10000000000, 400000000000), 2),
            "net_income": round(random.uniform(1000000000, 100000000000), 2),
            "eps": round(random.uniform(1.5, 15.0), 2),
            "pe_ratio": round(random.uniform(8, 45), 2),
            "pb_ratio": round(random.uniform(1.0, 12.0), 2),
            "debt_to_equity": round(random.uniform(0.1, 2.5), 2),
            "roe": round(random.uniform(5, 35), 2),
            "profit_margin": round(random.uniform(5, 40), 2),
            "revenue_growth_yoy": round(random.uniform(-10, 40), 2),
            "dividend_yield": round(random.uniform(0, 4), 2),
            "market_cap": round(random.uniform(50000000000, 3000000000000), 2),
            "beta": round(random.uniform(0.5, 2.0), 2),
            "provider": "demo_mock",
            "data_timestamp": datetime.now(timezone.utc).isoformat(),
            "data_freshness": "demo",
        }

    def get_provider_name(self) -> str:
        return "demo_mock"


class MockOnchainProvider(OnchainProvider):
    """Mock on-chain data provider for demo mode."""

    async def get_onchain_metrics(self, symbol: str) -> Dict[str, Any]:
        return {
            "symbol": symbol,
            "active_addresses": random.randint(300000, 1200000),
            "transaction_count": random.randint(500000, 2000000),
            "transaction_volume_usd": round(random.uniform(5000000000, 50000000000), 2),
            "tvl": round(random.uniform(1000000000, 80000000000), 2),
            "staking_ratio": round(random.uniform(0.15, 0.70), 4),
            "exchange_inflow": round(random.uniform(1000, 50000), 2),
            "exchange_outflow": round(random.uniform(800, 45000), 2),
            "whale_transactions": random.randint(50, 500),
            "holder_count": random.randint(100000, 50000000),
            "top_holder_pct": round(random.uniform(5, 40), 2),
            "developer_activity": round(random.uniform(20, 95), 2),
            "provider": "demo_mock",
            "data_timestamp": datetime.now(timezone.utc).isoformat(),
            "data_freshness": "demo",
        }

    def get_provider_name(self) -> str:
        return "demo_mock"


# Provider factory
def get_mock_providers() -> Dict[str, Any]:
    """Return all mock providers for demo mode."""
    return {
        "stock_market": MockMarketDataProvider("stock"),
        "crypto_market": MockMarketDataProvider("crypto"),
        "news": MockNewsProvider(),
        "fundamental": MockFundamentalProvider(),
        "onchain": MockOnchainProvider(),
    }
