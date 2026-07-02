import httpx
import os
import asyncio
from typing import List, Dict, Any
from .base import NewsProvider

class NewsAPIProvider(NewsProvider):
    """
    NewsAPI implementation for global financial news.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY", "")
        self.base_url = "https://newsapi.org/v2"
        self.client = httpx.AsyncClient(timeout=10.0)

    async def _fetch(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        if not self.api_key:
            return {"articles": []}
            
        params = {"apiKey": self.api_key}
        params.update(kwargs)
        
        try:
            response = await self.client.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # Fallback gracefully
            return {"articles": []}
            
    def _format_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": article.get("url"),
            "title": article.get("title", ""),
            "summary": article.get("description", ""),
            "content": article.get("content", ""),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", "Unknown"),
            "image_url": article.get("urlToImage", ""),
            "author": article.get("author", "")
        }

    async def get_latest_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        data = await self._fetch("top-headlines", category="business", language="en", pageSize=limit)
        articles = data.get("articles", [])
        return [self._format_article(a) for a in articles if a.get("title") != "[Removed]"]

    async def get_news_for_asset(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        # Map symbol to search term
        term = symbol.replace("USD", "")
        data = await self._fetch("everything", q=term, language="en", sortBy="publishedAt", pageSize=limit)
        articles = data.get("articles", [])
        return [self._format_article(a) for a in articles if a.get("title") != "[Removed]"]

    async def get_high_impact_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        # NewsAPI doesn't have impact natively, we simulate by filtering top business headlines
        data = await self._fetch("top-headlines", category="business", language="en", pageSize=limit)
        articles = data.get("articles", [])
        formatted = [self._format_article(a) for a in articles if a.get("title") != "[Removed]"]
        
        # Inject artificial impact score based on source for demonstration
        for f in formatted:
            f["impact_score"] = 90 if f["source"] in ["Bloomberg", "Reuters", "The Wall Street Journal"] else 75
            
        return formatted

    def get_provider_name(self) -> str:
        return "NewsAPI"

    async def close(self):
        await self.client.aclose()
