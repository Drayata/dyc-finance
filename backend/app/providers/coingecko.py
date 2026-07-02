import httpx
import os
import asyncio
from typing import List, Dict, Any
from .base import MarketDataProvider, FundamentalProvider

class CoinGeckoProvider(MarketDataProvider, FundamentalProvider):
    """
    CoinGecko API implementation for Cryptocurrencies.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COINGECKO_API_KEY", "")
        # Use pro api url if api key is provided, else use public api
        self.base_url = "https://pro-api.coingecko.com/api/v3" if self.api_key else "https://api.coingecko.com/api/v3"
        
        headers = {}
        if self.api_key:
            headers["x-cg-pro-api-key"] = self.api_key
            
        self.client = httpx.AsyncClient(timeout=10.0, headers=headers)
        self.coin_list = []
        
    async def _get_coin_id(self, symbol: str) -> str:
        symbol = symbol.lower().replace("usd", "")
        
        if not self.coin_list:
            response = await self.client.get(f"{self.base_url}/coins/list")
            response.raise_for_status()
            self.coin_list = response.json()
            
        # Try exact match
        for coin in self.coin_list:
            if coin["symbol"].lower() == symbol:
                return coin["id"]
                
        # Default fallback
        fallbacks = {"btc": "bitcoin", "eth": "ethereum", "sol": "solana"}
        return fallbacks.get(symbol, symbol)

    async def get_price(self, symbol: str) -> Dict[str, Any]:
        coin_id = await self._get_coin_id(symbol)
        response = await self.client.get(
            f"{self.base_url}/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_24hr_vol": "true"
            }
        )
        data = response.json()
        
        if coin_id not in data:
            return {}
            
        coin_data = data[coin_id]
        return {
            "symbol": symbol.upper(),
            "price": float(coin_data.get("usd", 0)),
            "change": 0.0, # CoinGecko doesn't provide absolute change in simple/price easily
            "change_percent": float(coin_data.get("usd_24h_change", 0)),
            "volume": float(coin_data.get("usd_24h_vol", 0)),
            "currency": "USD"
        }

    async def get_candles(self, symbol: str, interval: str = "1d", limit: int = 100) -> List[Dict[str, Any]]:
        coin_id = await self._get_coin_id(symbol)
        
        days = limit if interval == "1d" else "max"
        
        response = await self.client.get(
            f"{self.base_url}/coins/{coin_id}/ohlc",
            params={
                "vs_currency": "usd",
                "days": days
            }
        )
        data = response.json()
        
        if not isinstance(data, list):
            return []
            
        candles = []
        for item in data[-limit:]:
            candles.append({
                "timestamp": item[0],
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": 0 # CoinGecko OHLC doesn't include volume
            })
            
        return candles

    async def get_market_overview(self) -> Dict[str, Any]:
        response = await self.client.get(f"{self.base_url}/global")
        data = response.json().get("data", {})
        
        if not data:
            return {}
            
        return {
            "total_market_cap": data.get("total_market_cap", {}).get("usd", 0),
            "total_volume": data.get("total_volume", {}).get("usd", 0),
            "market_cap_percentage": data.get("market_cap_percentage", {})
        }

    async def get_movers(self) -> Dict[str, Any]:
        response = await self.client.get(
            f"{self.base_url}/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 100,
                "page": 1
            }
        )
        data = response.json()
        
        if not isinstance(data, list):
            return {"gainers": [], "losers": [], "active": []}
            
        sorted_by_change = sorted(data, key=lambda x: x.get("price_change_percentage_24h") or 0)
        
        def format_asset(item):
            return {
                "symbol": f"{item['symbol'].upper()}USD",
                "price": float(item.get("current_price", 0)),
                "change": float(item.get("price_change_24h", 0)),
                "change_percent": float(item.get("price_change_percentage_24h", 0))
            }
            
        return {
            "gainers": [format_asset(x) for x in reversed(sorted_by_change[-10:])],
            "losers": [format_asset(x) for x in sorted_by_change[:10]],
            "active": [format_asset(x) for x in data[:10]] # Top by market cap as proxy for active
        }

    async def search(self, query: str) -> List[Dict[str, Any]]:
        response = await self.client.get(f"{self.base_url}/search", params={"query": query})
        data = response.json()
        
        return [
            {
                "symbol": f"{coin['symbol'].upper()}USD",
                "name": coin['name'],
                "type": "crypto",
                "region": "global"
            }
            for coin in data.get("coins", [])[:10]
        ]

    async def get_fundamentals(self, symbol: str) -> Dict[str, Any]:
        coin_id = await self._get_coin_id(symbol)
        response = await self.client.get(
            f"{self.base_url}/coins/{coin_id}",
            params={"localization": "false", "tickers": "false", "market_data": "true", "community_data": "false", "developer_data": "false", "sparkline": "false"}
        )
        data = response.json()
        
        if "market_data" not in data:
            return {}
            
        md = data["market_data"]
        return {
            "market_cap": md.get("market_cap", {}).get("usd", 0),
            "fully_diluted_valuation": md.get("fully_diluted_valuation", {}).get("usd", 0),
            "circulating_supply": md.get("circulating_supply", 0),
            "total_supply": md.get("total_supply", 0),
            "max_supply": md.get("max_supply", 0),
            "all_time_high": md.get("ath", {}).get("usd", 0),
            "sector": "Cryptocurrency",
            "industry": data.get("categories", ["Unknown"])[0] if data.get("categories") else "Unknown"
        }

    def get_provider_name(self) -> str:
        return "CoinGecko"

    def get_data_freshness(self) -> str:
        return "delayed"

    async def close(self):
        await self.client.aclose()
