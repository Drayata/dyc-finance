"""
MarketPulse AI — Backend Tests
Tests covering API endpoints, analytics, providers, and security.
"""
import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import patch

# ==============================================================================
# Test: Technical Indicator Calculations
# ==============================================================================

class TestTechnicalIndicators:
    """Verify that technical indicators compute correctly."""

    def test_compute_sma(self):
        from app.analytics.technical import compute_sma
        prices = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        result = compute_sma(prices, 5)
        assert result is not None
        assert abs(result - 18.0) < 0.01  # Mean of [16,17,18,19,20]

    def test_compute_sma_insufficient_data(self):
        from app.analytics.technical import compute_sma
        result = compute_sma([10, 11], 5)
        assert result is None

    def test_compute_rsi(self):
        from app.analytics.technical import compute_rsi
        # Trending up strongly
        prices = list(range(100, 120))
        result = compute_rsi(prices, 14)
        assert result is not None
        assert result > 50  # Should be bullish

    def test_compute_rsi_insufficient_data(self):
        from app.analytics.technical import compute_rsi
        result = compute_rsi([10, 11, 12], 14)
        assert result is None

    def test_compute_macd(self):
        from app.analytics.technical import compute_macd
        prices = list(range(100, 150))
        result = compute_macd(prices)
        assert result["macd"] is not None
        assert "signal" in result
        assert "histogram" in result

    def test_compute_bollinger_bands(self):
        from app.analytics.technical import compute_bollinger_bands
        prices = list(range(100, 125))
        result = compute_bollinger_bands(prices, period=20)
        assert result["upper"] is not None
        assert result["middle"] is not None
        assert result["lower"] is not None
        assert result["upper"] > result["middle"] > result["lower"]

    def test_compute_atr(self):
        from app.analytics.technical import compute_atr
        highs = [i + 2 for i in range(100, 120)]
        lows = [i - 2 for i in range(100, 120)]
        closes = list(range(100, 120))
        result = compute_atr(highs, lows, closes, 14)
        assert result is not None
        assert result > 0

    def test_compute_all_indicators(self):
        from app.analytics.technical import compute_all_indicators
        import random
        random.seed(42)
        candles = []
        price = 100
        for i in range(60):
            price += random.uniform(-2, 2.5)
            candles.append({
                "timestamp": f"2024-01-{i+1:02d}T00:00:00Z",
                "open": price - 0.5,
                "high": price + 1,
                "low": price - 1,
                "close": price,
                "volume": 1000000,
            })
        result = compute_all_indicators(candles)
        assert "rsi_14" in result
        assert "macd" in result
        assert "sma_20" in result

    def test_compute_technical_score(self):
        from app.analytics.technical import compute_technical_score
        indicators = {
            "rsi_14": 35.0,
            "macd": 0.5,
            "macd_signal": 0.3,
            "sma_20": 100,
            "sma_50": 95,
            "bb_upper": 110,
            "bb_middle": 100,
            "bb_lower": 90,
            "adx": 30,
            "plus_di": 25,
            "minus_di": 15,
            "support_1": 95,
            "resistance_1": 105,
        }
        result = compute_technical_score(indicators, 102)
        assert "score" in result
        assert "confidence" in result
        assert "sub_scores" in result
        assert -100 <= result["score"] <= 100


# ==============================================================================
# Test: Signal Engine
# ==============================================================================

class TestSignalEngine:
    """Verify signal generation produces valid, compliant outputs."""

    def _make_candles(self, n=60):
        import random
        random.seed(123)
        candles = []
        price = 100
        for i in range(n):
            price += random.uniform(-2, 2.5)
            candles.append({
                "timestamp": f"2024-01-{(i%28)+1:02d}T00:00:00Z",
                "open": price - 0.5,
                "high": price + 1,
                "low": price - 1,
                "close": price,
                "volume": 1000000,
            })
        return candles

    def test_generate_signal_basic(self):
        from app.analytics.signal_engine import generate_signal_for_asset
        candles = self._make_candles()
        signal = generate_signal_for_asset("AAPL", "stock", candles)

        assert "direction" in signal
        assert signal["direction"] in ("strong_bullish", "bullish", "neutral", "bearish", "strong_bearish")
        assert "final_score" in signal
        assert -100 <= signal["final_score"] <= 100
        assert "confidence_score" in signal
        assert 0 <= signal["confidence_score"] <= 100
        assert "risk_level" in signal
        assert "disclaimer" in signal
        assert "guaranteed" not in signal["disclaimer"].lower()

    def test_signal_has_required_fields(self):
        from app.analytics.signal_engine import generate_signal_for_asset
        candles = self._make_candles()
        signal = generate_signal_for_asset("BTC", "crypto", candles)

        required_fields = [
            "symbol", "direction", "final_score", "confidence_score",
            "risk_level", "time_horizon", "price_at_signal",
            "expected_move_low", "expected_move_high",
            "technical_score", "bull_factors", "bear_factors",
            "key_risks", "invalidation_conditions", "disclaimer",
            "data_sources", "calculation_timestamp", "weights_used",
        ]
        for field in required_fields:
            assert field in signal, f"Missing required field: {field}"

    def test_signal_never_guarantees_profit(self):
        from app.analytics.signal_engine import generate_signal_for_asset, SIGNAL_DISCLAIMER
        candles = self._make_candles()
        signal = generate_signal_for_asset("AAPL", "stock", candles)

        forbidden_phrases = [
            "guaranteed to increase", "guaranteed profit", "must buy",
            "impossible to lose", "risk-free", "guaranteed investment return",
        ]
        disclaimer = signal.get("disclaimer", "").lower()
        for phrase in forbidden_phrases:
            assert phrase not in disclaimer, f"Forbidden phrase found: {phrase}"

    def test_signal_with_news(self):
        from app.analytics.signal_engine import generate_signal_for_asset
        candles = self._make_candles()
        news = [
            {"title": "Positive earnings", "overall_sentiment": 0.7, "impact_score": 80, "source_name": "test"},
        ]
        signal = generate_signal_for_asset("AAPL", "stock", candles, news_data=news)
        assert signal["news_score"] != 0

    def test_signal_insufficient_data(self):
        from app.analytics.signal_engine import generate_signal_for_asset
        candles = [{"close": 100, "high": 101, "low": 99, "open": 100, "volume": 1000}] * 5
        result = generate_signal_for_asset("TEST", "stock", candles)
        assert "error" in result

    def test_signal_classification(self):
        from app.analytics.signal_engine import classify_signal
        assert classify_signal(80) == "strong_bullish"
        assert classify_signal(50) == "bullish"
        assert classify_signal(0) == "neutral"
        assert classify_signal(-50) == "bearish"
        assert classify_signal(-80) == "strong_bearish"


# ==============================================================================
# Test: Mock Provider
# ==============================================================================

class TestMockProvider:
    """Verify mock providers return properly labeled demo data."""

    @pytest.mark.asyncio
    async def test_mock_price_labeled_as_demo(self):
        from app.providers.mock_provider import MockMarketDataProvider
        provider = MockMarketDataProvider("stock")
        price = await provider.get_price("AAPL")
        assert price["provider"] == "demo_mock"
        assert price["data_freshness"] == "demo"

    @pytest.mark.asyncio
    async def test_mock_candles_returned(self):
        from app.providers.mock_provider import MockMarketDataProvider
        provider = MockMarketDataProvider("crypto")
        candles = await provider.get_candles("BTC", interval="1d", limit=30)
        assert len(candles) > 0
        assert "open" in candles[0]
        assert "close" in candles[0]

    @pytest.mark.asyncio
    async def test_mock_overview(self):
        from app.providers.mock_provider import MockMarketDataProvider
        provider = MockMarketDataProvider("stock")
        overview = await provider.get_market_overview()
        assert overview["demo_mode"] is True
        assert "indices" in overview

    @pytest.mark.asyncio
    async def test_mock_news_labeled(self):
        from app.providers.mock_provider import MockNewsProvider
        provider = MockNewsProvider()
        news = await provider.get_latest_news(10)
        assert len(news) > 0
        assert "title" in news[0]
        assert "impact_score" in news[0]

    @pytest.mark.asyncio
    async def test_mock_search(self):
        from app.providers.mock_provider import MockMarketDataProvider
        provider = MockMarketDataProvider("stock")
        results = await provider.search("apple")
        assert len(results) > 0
        assert results[0]["symbol"] == "AAPL"

    @pytest.mark.asyncio
    async def test_mock_never_mixes_with_real(self):
        """Mock data must never be mistaken for real data."""
        from app.providers.mock_provider import MockMarketDataProvider
        provider = MockMarketDataProvider("stock")
        price = await provider.get_price("AAPL")
        assert price["data_status"] == "demo"
        assert provider.get_data_freshness() == "demo"


# ==============================================================================
# Test: Security
# ==============================================================================

class TestSecurity:
    """Verify authentication and security controls."""

    def test_password_hashing(self):
        from app.security import hash_password, verify_password
        hashed = hash_password("TestPass123!")
        assert verify_password("TestPass123!", hashed)
        assert not verify_password("WrongPassword", hashed)

    def test_jwt_token_creation(self):
        from app.security import create_access_token, decode_token
        token = create_access_token("test-user-id", "user")
        payload = decode_token(token)
        assert payload["sub"] == "test-user-id"
        assert payload["role"] == "user"
        assert payload["type"] == "access"

    def test_jwt_refresh_token(self):
        from app.security import create_refresh_token, decode_token
        token = create_refresh_token("test-user-id")
        payload = decode_token(token)
        assert payload["sub"] == "test-user-id"
        assert payload["type"] == "refresh"

    def test_password_validation(self):
        from app.security import validate_password
        from fastapi import HTTPException

        # Should pass
        validate_password("StrongPass1")

        # Should fail - too short
        with pytest.raises(HTTPException):
            validate_password("Ab1")

        # Should fail - no uppercase
        with pytest.raises(HTTPException):
            validate_password("weakpassword1")

        # Should fail - no digit
        with pytest.raises(HTTPException):
            validate_password("NoDigitHere")


# ==============================================================================
# Test: Data Quality Rules
# ==============================================================================

class TestDataQuality:
    """Verify data quality and anti-hallucination rules."""

    def test_every_price_has_provider(self):
        """Rule 1: Every numerical value must come from a verified source."""
        import asyncio
        from app.providers.mock_provider import MockMarketDataProvider
        provider = MockMarketDataProvider("stock")
        price = asyncio.get_event_loop().run_until_complete(provider.get_price("AAPL"))
        assert "provider" in price
        assert price["provider"] != ""

    def test_every_article_has_source(self):
        """Rule 2: Every article must include a source."""
        from app.providers.mock_provider import MOCK_NEWS
        for article in MOCK_NEWS:
            assert "source_name" in article
            assert article["source_name"] != ""

    def test_every_article_has_timestamp(self):
        """Rule 4: Every output must include a timestamp."""
        from app.providers.mock_provider import MOCK_NEWS
        for article in MOCK_NEWS:
            assert "published_at" in article

    def test_rumors_labeled_unverified(self):
        """Rule 5: Rumors must be labeled as unverified."""
        from app.providers.mock_provider import MOCK_NEWS
        rumors = [n for n in MOCK_NEWS if n.get("event_category") == "rumor"]
        for rumor in rumors:
            assert rumor["is_verified"] is False

    def test_signal_has_data_sources(self):
        """Signals must reference their data sources."""
        from app.analytics.signal_engine import generate_signal_for_asset
        import random
        random.seed(42)
        candles = []
        price = 100
        for i in range(60):
            price += random.uniform(-2, 2.5)
            candles.append({"timestamp": f"2024-01-{(i%28)+1:02d}", "open": price-0.5, "high": price+1, "low": price-1, "close": price, "volume": 1000000})
        signal = generate_signal_for_asset("AAPL", "stock", candles)
        assert "data_sources" in signal
        assert len(signal["data_sources"]) > 0
