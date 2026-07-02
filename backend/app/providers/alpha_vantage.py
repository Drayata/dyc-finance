import httpx
import os
import asyncio
from typing import List, Dict, Any
from .base import MarketDataProvider, FundamentalProvider

class AlphaVantageProvider(MarketDataProvider, FundamentalProvider):
    """
    Alpha Vantage API implementation for US Equities.
    Uses httpx for async requests.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
        self.base_url = "https://www.alphavantage.co/query"
        self.client = httpx.AsyncClient(timeout=10.0)

    async def _fetch(self, function: str, symbol: str = None, **kwargs) -> Dict[str, Any]:
        params = {
            "function": function,
            "apikey": self.api_key
        }
        if symbol:
            params["symbol"] = symbol
        params.update(kwargs)
        
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if "Error Message" in data:
                raise ValueError(f"Alpha Vantage API error: {data['Error Message']}")
            if "Note" in data:
                # Rate limit hit (Standard API is 25 requests/day)
                raise ValueError(f"Alpha Vantage rate limit: {data['Note']}")
            return data
        except Exception as e:
            raise ValueError(f"Failed to fetch from Alpha Vantage: {str(e)}")

    async def get_price(self, symbol: str) -> Dict[str, Any]:
        data = await self._fetch("GLOBAL_QUOTE", symbol)
        quote = data.get("Global Quote", {})
        if not quote:
            return {}
            
        return {
            "symbol": quote.get("01. symbol"),
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": float(quote.get("10. change percent", "0%").strip("%")),
            "volume": int(quote.get("06. volume", 0)),
            "currency": "USD"
        }

    async def get_candles(self, symbol: str, interval: str = "1d", limit: int = 100) -> List[Dict[str, Any]]:
        if interval == "1d":
            function = "TIME_SERIES_DAILY"
            data_key = "Time Series (Daily)"
        elif interval == "1wk":
            function = "TIME_SERIES_WEEKLY"
            data_key = "Weekly Time Series"
        else:
            function = "TIME_SERIES_INTRADAY"
            data_key = f"Time Series ({interval})"
            
        params = {}
        if function == "TIME_SERIES_INTRADAY":
            params["interval"] = interval
            
        data = await self._fetch(function, symbol, **params)
        time_series = data.get(data_key, {})
        
        candles = []
        for ts, values in list(time_series.items())[:limit]:
            candles.append({
                "timestamp": ts,
                "open": float(values.get("1. open", 0)),
                "high": float(values.get("2. high", 0)),
                "low": float(values.get("3. low", 0)),
                "close": float(values.get("4. close", 0)),
                "volume": int(values.get("5. volume", 0))
            })
            
        # Reverse to get chronological order
        return list(reversed(candles))

    async def get_market_overview(self) -> Dict[str, Any]:
        # AlphaVantage doesn't have a single "overview" endpoint that returns indices easily without multiple calls
        # We'll return empty for now, the registry will merge with mock provider
        return {}

    async def get_movers(self) -> Dict[str, Any]:
        data = await self._fetch("TOP_GAINERS_LOSERS")
        
        def format_asset(item):
            return {
                "symbol": item.get("ticker"),
                "price": float(item.get("price", 0)),
                "change": float(item.get("change_amount", 0)),
                "change_percent": float(item.get("change_percentage", "0%").strip("%"))
            }
            
        return {
            "gainers": [format_asset(x) for x in data.get("top_gainers", [])[:10]],
            "losers": [format_asset(x) for x in data.get("top_losers", [])[:10]],
            "active": [format_asset(x) for x in data.get("most_actively_traded", [])[:10]]
        }

    async def search(self, query: str) -> List[Dict[str, Any]]:
        data = await self._fetch("SYMBOL_SEARCH", keywords=query)
        matches = data.get("bestMatches", [])
        return [
            {
                "symbol": match.get("1. symbol"),
                "name": match.get("2. name"),
                "type": match.get("3. type"),
                "region": match.get("4. region")
            }
            for match in matches
        ]
        
    async def get_fundamentals(self, symbol: str) -> Dict[str, Any]:
        data = await self._fetch("OVERVIEW", symbol)
        if not data or "Symbol" not in data:
            return {}
            
        return {
            "market_cap": float(data.get("MarketCapitalization", 0)),
            "pe_ratio": float(data.get("PERatio", 0)) if data.get("PERatio", "None") != "None" else None,
            "pb_ratio": float(data.get("PriceToBookRatio", 0)) if data.get("PriceToBookRatio", "None") != "None" else None,
            "dividend_yield": float(data.get("DividendYield", 0)) if data.get("DividendYield", "None") != "None" else 0.0,
            "eps": float(data.get("EPS", 0)) if data.get("EPS", "None") != "None" else None,
            "sector": data.get("Sector", "Unknown"),
            "industry": data.get("Industry", "Unknown")
        }

    def get_provider_name(self) -> str:
        return "Alpha Vantage"

    def get_data_freshness(self) -> str:
        return "end_of_day"

    async def close(self):
        await self.client.aclose()
