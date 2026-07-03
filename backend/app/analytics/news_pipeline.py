import re
import hashlib
from typing import List, Dict, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NewsPipeline:
    """
    10-Stage NLP Pipeline for analyzing financial news.
    Uses basic heuristics and lightweight NLP for the MVP.
    """
    
    def __init__(self):
        # Basic dictionaries for sentiment (to be replaced with FinBERT in future)
        self.bullish_keywords = {"surge", "jump", "record", "profit", "beat", "upgrade", "growth", "buy", "bull", "rally", "outperform"}
        self.bearish_keywords = {"plunge", "drop", "loss", "miss", "downgrade", "decline", "sell", "bear", "crash", "investigation", "lawsuit"}
        
        # Entities matching
        self.known_entities = {
            "apple": "AAPL", "aapl": "AAPL", "iphone": "AAPL",
            "microsoft": "MSFT", "msft": "MSFT", "windows": "MSFT",
            "nvidia": "NVDA", "nvda": "NVDA", "gpu": "NVDA",
            "bitcoin": "BTC", "btc": "BTC",
            "ethereum": "ETH", "eth": "ETH"
        }

    def _hash_content(self, text: str) -> str:
        """Stage 2: Deduplication hash"""
        return hashlib.md5(text.encode('utf-8')).hexdight()

    def _extract_entities(self, text: str) -> List[str]:
        """Stage 3: Entity Extraction (Mock spaCy NER)"""
        words = set(re.findall(r'\b\w+\b', text.lower()))
        entities = []
        for word in words:
            if word in self.known_entities:
                entities.append(self.known_entities[word])
        return list(set(entities))

    def _classify_event(self, text: str) -> str:
        """Stage 4: Event Classification"""
        text = text.lower()
        if "earnings" in text or "profit" in text or "revenue" in text:
            return "Earnings Report"
        if "merger" in text or "acquisition" in text or "buyout" in text:
            return "M&A"
        if "lawsuit" in text or "sec " in text or "sued" in text or "investigation" in text:
            return "Regulatory / Legal"
        if "launch" in text or "release" in text or "new product" in text:
            return "Product Launch"
        if "upgrade" in text or "downgrade" in text or "target" in text:
            return "Analyst Rating"
        return "General Market News"

    def _calculate_sentiment(self, text: str) -> Tuple[float, str]:
        """Stage 6: Sentiment Scoring"""
        words = re.findall(r'\b\w+\b', text.lower())
        bull_count = sum(1 for w in words if w in self.bullish_keywords)
        bear_count = sum(1 for w in words if w in self.bearish_keywords)
        
        total_matched = bull_count + bear_count
        if total_matched == 0:
            return 0.0, "Neutral"
            
        score = (bull_count - bear_count) / total_matched
        
        if score > 0.3:
            label = "Positive"
        elif score < -0.3:
            label = "Negative"
        else:
            label = "Neutral"
            
        return score, label

    def _calculate_impact(self, event_type: str, sentiment_abs: float) -> int:
        """Stage 7: Event Impact Scoring"""
        base_impact = {
            "Earnings Report": 80,
            "M&A": 90,
            "Regulatory / Legal": 85,
            "Product Launch": 60,
            "Analyst Rating": 50,
            "General Market News": 30
        }
        
        impact = base_impact.get(event_type, 30)
        # Higher absolute sentiment increases impact
        impact += int(sentiment_abs * 20)
        return min(impact, 100)

    def _estimate_horizon(self, event_type: str) -> str:
        """Stage 9: Time Horizon estimation"""
        horizons = {
            "Earnings Report": "1-4 Weeks",
            "M&A": "3-6 Months",
            "Regulatory / Legal": "1-3 Months",
            "Product Launch": "1-4 Weeks",
            "Analyst Rating": "1-5 Days",
            "General Market News": "1-3 Days"
        }
        return horizons.get(event_type, "1-3 Days")

    def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single article through the 10-stage pipeline.
        """
        text_to_analyze = f"{article.get('title', '')} {article.get('summary', '')} {article.get('content', '')}"
        
        # Stages 1-2: Ingestion & Deduplication
        content_hash = self._hash_content(text_to_analyze)
        
        # Stage 3: Entity Extraction
        entities = self._extract_entities(text_to_analyze)
        
        # Stage 4: Event Classification
        event_type = self._classify_event(text_to_analyze)
        
        # Stage 5 & 6: Relevance & Sentiment
        # For MVP, relevance is 100 if we found a known entity, else 50
        relevance = 100 if entities else 50
        sentiment_score, sentiment_label = self._calculate_sentiment(text_to_analyze)
        
        # Stage 7 & 8: Impact & Direction
        impact_score = self._calculate_impact(event_type, abs(sentiment_score))
        direction = "Bullish" if sentiment_score > 0 else "Bearish" if sentiment_score < 0 else "Neutral"
        
        # Stage 9: Time Horizon
        horizon = self._estimate_horizon(event_type)
        
        # Stage 10: Explanation Generation
        explanation = f"Article indicates {sentiment_label.lower()} sentiment related to {event_type}. "
        explanation += f"Impact assessed as {impact_score}/100 with a {horizon} horizon."
        
        return {
            "id": article.get("id"),
            "title": article.get("title"),
            "url": article.get("url"),
            "published_at": article.get("published_at"),
            "source": article.get("source"),
            "content_hash": content_hash,
            "entities": entities,
            "event_type": event_type,
            "relevance_score": relevance,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
            "impact_score": impact_score,
            "direction": direction,
            "time_horizon": horizon,
            "explanation": explanation
        }

    def process_batch(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        seen_hashes = set()
        
        for article in articles:
            result = self.process_article(article)
            # Stage 2 implementation (Deduplication)
            if result["content_hash"] not in seen_hashes:
                seen_hashes.add(result["content_hash"])
                results.append(result)
                
        return results

news_pipeline = NewsPipeline()
