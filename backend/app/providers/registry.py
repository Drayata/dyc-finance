import os
from typing import Dict, Any, Type, Optional

from app.config import settings
from .base import MarketDataProvider, NewsProvider, FundamentalProvider, OnchainProvider
from .mock_provider import MockMarketProvider, MockNewsProvider, MockFundamentalProvider, MockOnchainProvider
from .alpha_vantage import AlphaVantageProvider
from .coingecko import CoinGeckoProvider
from .newsapi import NewsAPIProvider

class ProviderRegistry:
    """
    Factory for instantiating the correct provider based on configuration
    and asset type. Handles fallback to mock providers if production
    providers fail or are disabled.
    """
    
    def __init__(self):
        self.use_mock = settings.USE_MOCK_DATA
        
        # Initialize singletons for providers
        self._mock_market = MockMarketProvider()
        self._mock_news = MockNewsProvider()
        self._mock_fundamental = MockFundamentalProvider()
        self._mock_onchain = MockOnchainProvider()
        
        self._alpha_vantage = None
        self._coingecko = None
        self._newsapi = None
        
    def _get_alpha_vantage(self) -> AlphaVantageProvider:
        if not self._alpha_vantage:
            self._alpha_vantage = AlphaVantageProvider()
        return self._alpha_vantage
        
    def _get_coingecko(self) -> CoinGeckoProvider:
        if not self._coingecko:
            self._coingecko = CoinGeckoProvider()
        return self._coingecko
        
    def _get_newsapi(self) -> NewsAPIProvider:
        if not self._newsapi:
            self._newsapi = NewsAPIProvider()
        return self._newsapi

    def get_market_provider(self, asset_type: str = "stock") -> MarketDataProvider:
        """Get the appropriate market data provider for the asset type."""
        if self.use_mock:
            return self._mock_market
            
        if asset_type.lower() == "crypto":
            return self._get_coingecko()
        elif asset_type.lower() in ["stock", "index", "etf"]:
            return self._get_alpha_vantage()
        else:
            return self._mock_market # Fallback

    def get_news_provider(self) -> NewsProvider:
        """Get the news provider."""
        if self.use_mock:
            return self._mock_news
            
        return self._get_newsapi()

    def get_fundamental_provider(self, asset_type: str = "stock") -> FundamentalProvider:
        """Get fundamental data provider."""
        if self.use_mock:
            return self._mock_fundamental
            
        if asset_type.lower() == "crypto":
            return self._get_coingecko()
        else:
            return self._get_alpha_vantage()

    def get_onchain_provider(self) -> OnchainProvider:
        """Get onchain metrics provider (crypto only)."""
        # We don't have a production onchain provider yet (like Glassnode)
        # So we always return mock for now
        return self._mock_onchain

    async def close_all(self):
        """Close all active provider HTTP clients."""
        if self._alpha_vantage:
            await self._alpha_vantage.close()
        if self._coingecko:
            await self._coingecko.close()
        if self._newsapi:
            await self._newsapi.close()

# Global registry instance
registry = ProviderRegistry()
