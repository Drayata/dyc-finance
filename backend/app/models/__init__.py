"""
MarketPulse AI — Database Models Package
Comprehensive schema covering all 40+ tables.
"""
from app.models.auth import User, Role, UserSession, Subscription
from app.models.market import (
    Asset, Exchange, AssetPair, MarketPrice, MarketCandle,
    MarketSnapshot, Fundamental, TechnicalIndicator,
    OnchainMetric, DerivativesMetric,
)
from app.models.news import (
    NewsSource, NewsArticle, NewsEntity, NewsAssetRelation,
    Event, EventImpact, SentimentResult,
)
from app.models.signals import (
    Signal, SignalComponent, SignalExplanation, SignalOutcome,
)
from app.models.ml import (
    ModelVersion, ModelMetric, BacktestRun, BacktestResult,
)
from app.models.user_features import (
    Watchlist, WatchlistItem, AlertRule, AlertEvent, Notification,
)
from app.models.ops import (
    DataProvider, ProviderHealth, IngestionJob, DataQualityLog, AuditLog,
)

__all__ = [
    "User", "Role", "UserSession", "Subscription",
    "Asset", "Exchange", "AssetPair", "MarketPrice", "MarketCandle",
    "MarketSnapshot", "Fundamental", "TechnicalIndicator",
    "OnchainMetric", "DerivativesMetric",
    "NewsSource", "NewsArticle", "NewsEntity", "NewsAssetRelation",
    "Event", "EventImpact", "SentimentResult",
    "Signal", "SignalComponent", "SignalExplanation", "SignalOutcome",
    "ModelVersion", "ModelMetric", "BacktestRun", "BacktestResult",
    "Watchlist", "WatchlistItem", "AlertRule", "AlertEvent", "Notification",
    "DataProvider", "ProviderHealth", "IngestionJob", "DataQualityLog", "AuditLog",
]
