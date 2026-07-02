"""
MarketPulse AI — News Intelligence Models
Covers the full 10-stage news pipeline: sources, articles, entities, events, sentiment.
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Text, Integer,
    Float, Numeric, Enum as SAEnum, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base


class SourceCredibility(str, enum.Enum):
    OFFICIAL = "official"         # Regulator, exchange, central bank
    PRIMARY = "primary"           # Company IR, official press release
    MAJOR_MEDIA = "major_media"   # Reuters, Bloomberg, CNBC
    SPECIALIZED = "specialized"   # CoinDesk, The Block, Bisnis Indonesia
    GENERAL = "general"           # General news outlets
    SOCIAL = "social"             # Social media, forums
    UNVERIFIED = "unverified"     # Unknown or unverified sources


class EventCategory(str, enum.Enum):
    EARNINGS = "earnings"
    REVENUE_GUIDANCE = "revenue_guidance"
    DIVIDEND = "dividend"
    STOCK_SPLIT = "stock_split"
    MERGER_ACQUISITION = "merger_acquisition"
    IPO = "ipo"
    SHARE_BUYBACK = "share_buyback"
    MANAGEMENT_CHANGE = "management_change"
    PRODUCT_LAUNCH = "product_launch"
    CYBERSECURITY_INCIDENT = "cybersecurity_incident"
    LAWSUIT = "lawsuit"
    REGULATORY_ACTION = "regulatory_action"
    MONETARY_POLICY = "monetary_policy"
    INTEREST_RATE = "interest_rate"
    INFLATION_DATA = "inflation_data"
    EMPLOYMENT_DATA = "employment_data"
    CURRENCY_MOVEMENT = "currency_movement"
    COMMODITY_MOVEMENT = "commodity_movement"
    GEOPOLITICAL_CONFLICT = "geopolitical_conflict"
    SUPPLY_CHAIN = "supply_chain"
    EXCHANGE_LISTING = "exchange_listing"
    EXCHANGE_DELISTING = "exchange_delisting"
    TOKEN_UNLOCK = "token_unlock"
    TOKEN_BURN = "token_burn"
    PROTOCOL_UPGRADE = "protocol_upgrade"
    SECURITY_EXPLOIT = "security_exploit"
    STABLECOIN_DEPEG = "stablecoin_depeg"
    ETF_FLOW = "etf_flow"
    WHALE_TRANSACTION = "whale_transaction"
    ONCHAIN_ANOMALY = "onchain_anomaly"
    STRATEGIC_PARTNERSHIP = "strategic_partnership"
    RUMOR = "rumor"
    UNVERIFIED_INFO = "unverified_info"
    OTHER = "other"


class ImpactDirection(str, enum.Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    MIXED = "mixed"
    UNCERTAIN = "uncertain"


class ImpactTimeHorizon(str, enum.Enum):
    IMMEDIATE = "immediate"       # < 24 hours
    SHORT_TERM = "short_term"     # 1-7 days
    SWING = "swing"               # 1-4 weeks
    MEDIUM_TERM = "medium_term"   # 1-6 months
    STRUCTURAL = "structural"     # > 6 months


class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(500))
    source_type = Column(String(50))  # api, rss, official, scraper
    credibility = Column(SAEnum(SourceCredibility), default=SourceCredibility.GENERAL)
    credibility_score = Column(Float, default=50.0)  # 0-100
    language = Column(String(10), default="en")
    country = Column(String(100))
    categories = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    requires_license = Column(Boolean, default=False)
    license_status = Column(String(50))  # compliant, pending, na
    rate_limit_per_minute = Column(Integer, default=60)
    last_fetched_at = Column(DateTime(timezone=True))
    fetch_interval_minutes = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    articles = relationship("NewsArticle", back_populates="source")


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("news_sources.id"), nullable=False, index=True)
    external_id = Column(String(500))  # Provider's article ID
    canonical_url = Column(String(1000), unique=True)
    title = Column(Text, nullable=False)
    summary = Column(Text)  # System-generated or provider summary (not full article text per licensing)
    author = Column(String(255))
    language = Column(String(10), default="en")
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    ingestion_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    # NLP Analysis Results (Stage 5-9)
    relevance_score = Column(Float)          # 0-100
    headline_sentiment = Column(Float)       # -1 to +1
    body_sentiment = Column(Float)           # -1 to +1
    overall_sentiment = Column(Float)        # -1 to +1
    uncertainty_score = Column(Float)        # 0-1
    emotional_intensity = Column(Float)      # 0-1
    impact_score = Column(Float)             # 0-100
    impact_direction = Column(SAEnum(ImpactDirection))
    impact_time_horizon = Column(SAEnum(ImpactTimeHorizon))
    impact_pathway = Column(Text)            # Logical chain of expected impact
    surprise_factor = Column(Float)          # 0-1
    novelty_score = Column(Float)            # 0-1 (is this genuinely new information?)
    already_priced_in = Column(Boolean, default=False)

    # Event classification
    event_category = Column(SAEnum(EventCategory))
    event_attributes = Column(JSONB)  # e.g., {"earnings_beat": true, "eps_actual": 2.5}

    # Deduplication
    content_hash = Column(String(64), index=True)
    duplicate_cluster_id = Column(UUID(as_uuid=True))
    is_primary_in_cluster = Column(Boolean, default=True)

    # Data quality
    is_verified = Column(Boolean, default=True)
    data_quality_score = Column(Float, default=50.0)
    source_credibility_score = Column(Float)
    processing_status = Column(String(20), default="pending")  # pending, processed, failed, skipped

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_article_published", "published_at"),
        Index("ix_article_event", "event_category"),
        Index("ix_article_impact", "impact_score"),
    )

    source = relationship("NewsSource", back_populates="articles")
    entities = relationship("NewsEntity", back_populates="article", cascade="all, delete-orphan")
    asset_relations = relationship("NewsAssetRelation", back_populates="article", cascade="all, delete-orphan")
    event_impacts = relationship("EventImpact", back_populates="article", cascade="all, delete-orphan")


class NewsEntity(Base):
    """Extracted entities from news articles (Stage 3)."""
    __tablename__ = "news_entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # company, ticker, crypto, sector, country, regulator, etc.
    entity_value = Column(String(500), nullable=False)
    entity_normalized = Column(String(500))  # Normalized/canonical form
    confidence = Column(Float, default=0.5)
    is_primary = Column(Boolean, default=False)  # Is this the main subject?
    sentiment = Column(Float)  # Entity-specific sentiment -1 to +1
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_entity_type_value", "entity_type", "entity_value"),
    )

    article = relationship("NewsArticle", back_populates="entities")


class NewsAssetRelation(Base):
    """Mapping between news articles and affected assets."""
    __tablename__ = "news_asset_relations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    relevance_score = Column(Float, default=50.0)  # 0-100
    is_primary_subject = Column(Boolean, default=False)
    expected_direction = Column(SAEnum(ImpactDirection))
    expected_magnitude = Column(Float)  # 0-100
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("article_id", "asset_id", name="uq_article_asset"),
    )

    article = relationship("NewsArticle", back_populates="asset_relations")
    asset = relationship("Asset", back_populates="news_relations")


class Event(Base):
    """Grouped event from multiple news articles."""
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text)
    category = Column(SAEnum(EventCategory), nullable=False)
    severity = Column(String(20))  # low, medium, high, critical
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))  # null = ongoing
    is_ongoing = Column(Boolean, default=True)
    source_count = Column(Integer, default=1)
    confirmation_level = Column(String(20), default="unconfirmed")  # unconfirmed, reported, confirmed, official
    affected_assets = Column(JSONB)  # Quick lookup: [{"symbol": "AAPL", "direction": "bearish"}]
    affected_sectors = Column(ARRAY(String))
    affected_countries = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    impacts = relationship("EventImpact", back_populates="event", cascade="all, delete-orphan")


class EventImpact(Base):
    """Estimated impact of an event on specific assets."""
    __tablename__ = "event_impacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id", ondelete="SET NULL"), index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), index=True)
    direction = Column(SAEnum(ImpactDirection), nullable=False)
    magnitude = Column(Float)  # 0-100
    time_horizon = Column(SAEnum(ImpactTimeHorizon))
    impact_pathway = Column(Text)  # Logical chain
    confidence = Column(Float, default=0.5)
    is_priced_in = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    event = relationship("Event", back_populates="impacts")
    article = relationship("NewsArticle", back_populates="event_impacts")


class SentimentResult(Base):
    """Aggregated sentiment for an asset over time."""
    __tablename__ = "sentiment_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    period = Column(String(20))  # 1h, 4h, 1d, 1w

    overall_sentiment = Column(Float)  # -1 to +1
    news_sentiment = Column(Float)
    social_sentiment = Column(Float)
    article_count = Column(Integer, default=0)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    average_impact = Column(Float)
    sentiment_change = Column(Float)  # vs previous period

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_sentiment_asset_ts", "asset_id", "timestamp"),
    )
