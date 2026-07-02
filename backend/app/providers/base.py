"""
MarketPulse AI — Provider Base Interfaces
Abstract base classes defining the adapter pattern for all data providers.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime


class MarketDataProvider(ABC):
    """Interface for stock and crypto market data providers."""

    @abstractmethod
    async def get_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for a symbol."""
        pass

    @abstractmethod
    async def get_candles(
        self, symbol: str, interval: str = "1d", limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get OHLCV candlestick data."""
        pass

    @abstractmethod
    async def get_market_overview(self) -> Dict[str, Any]:
        """Get market overview/summary."""
        pass

    @abstractmethod
    async def get_movers(self) -> Dict[str, Any]:
        """Get top gainers, losers, most active."""
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """Search for assets."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass

    @abstractmethod
    def get_data_freshness(self) -> str:
        """Return: real_time, delayed, end_of_day, estimated."""
        pass


class NewsProvider(ABC):
    """Interface for news data providers."""

    @abstractmethod
    async def get_latest_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_news_for_asset(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_high_impact_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass


class FundamentalProvider(ABC):
    """Interface for fundamental data providers."""

    @abstractmethod
    async def get_fundamentals(self, symbol: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass


class OnchainProvider(ABC):
    """Interface for on-chain data providers."""

    @abstractmethod
    async def get_onchain_metrics(self, symbol: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass
