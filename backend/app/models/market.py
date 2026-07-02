"""
MarketPulse AI — Market Data Models
Covers assets, exchanges, prices, candles, fundamentals, technicals, on-chain, and derivatives.
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Text, Integer,
    Float, Numeric, Enum as SAEnum, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class AssetType(str, enum.Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    INDEX = "index"
    ETF = "etf"
    FOREX = "forex"
    COMMODITY = "commodity"


class MarketStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PRE_MARKET = "pre_market"
    AFTER_HOURS = "after_hours"
    HALTED = "halted"


class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100))
    timezone = Column(String(50))
    currency = Column(String(10))
    market_open = Column(String(10))  # HH:MM format
    market_close = Column(String(10))
    status = Column(SAEnum(MarketStatus), default=MarketStatus.CLOSED)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    assets = relationship("Asset", back_populates="exchange")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    asset_type = Column(SAEnum(AssetType), nullable=False, index=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id"), index=True)
    sector = Column(String(100))
    industry = Column(String(100))
    country = Column(String(100))
    currency = Column(String(10))
    description = Column(Text)
    logo_url = Column(String(500))
    website = Column(String(500))

    # Crypto-specific
    blockchain = Column(String(100))
    contract_address = Column(String(255))
    max_supply = Column(Numeric(precision=30, scale=10))
    circulating_supply = Column(Numeric(precision=30, scale=10))

    # Data quality
    is_active = Column(Boolean, default=True)
    is_tradable = Column(Boolean, default=True)
    data_quality_score = Column(Float, default=50.0)
    has_sufficient_history = Column(Boolean, default=True)
    liquidity_tier = Column(String(20), default="medium")  # high, medium, low, very_low

    # Warnings
    manipulation_risk = Column(Boolean, default=False)
    unverified_contract = Column(Boolean, default=False)
    low_liquidity_warning = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("symbol", "asset_type", "exchange_id", name="uq_asset_symbol_type_exchange"),
        Index("ix_asset_type_sector", "asset_type", "sector"),
    )

    exchange = relationship("Exchange", back_populates="assets")
    prices = relationship("MarketPrice", back_populates="asset", cascade="all, delete-orphan")
    candles = relationship("MarketCandle", back_populates="asset", cascade="all, delete-orphan")
    fundamentals = relationship("Fundamental", back_populates="asset", cascade="all, delete-orphan")
    signals = relationship("Signal", back_populates="asset", cascade="all, delete-orphan")
    news_relations = relationship("NewsAssetRelation", back_populates="asset", cascade="all, delete-orphan")
    watchlist_items = relationship("WatchlistItem", back_populates="asset", cascade="all, delete-orphan")


class AssetPair(Base):
    __tablename__ = "asset_pairs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    base_asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    quote_asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    symbol = Column(String(50), nullable=False, index=True)
    exchange_id = Column(UUID(as_uuid=True), ForeignKey("exchanges.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("base_asset_id", "quote_asset_id", "exchange_id", name="uq_pair"),
    )


class MarketPrice(Base):
    """Latest price snapshot for an asset."""
    __tablename__ = "market_prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    price = Column(Numeric(precision=20, scale=8), nullable=False)
    price_change_24h = Column(Numeric(precision=20, scale=8))
    price_change_pct_24h = Column(Float)
    volume_24h = Column(Numeric(precision=30, scale=8))
    market_cap = Column(Numeric(precision=30, scale=2))
    high_24h = Column(Numeric(precision=20, scale=8))
    low_24h = Column(Numeric(precision=20, scale=8))
    open_24h = Column(Numeric(precision=20, scale=8))
    bid = Column(Numeric(precision=20, scale=8))
    ask = Column(Numeric(precision=20, scale=8))
    currency = Column(String(10), default="USD")

    # Data provenance
    provider = Column(String(50), nullable=False)
    source_url = Column(String(500))
    data_timestamp = Column(DateTime(timezone=True), nullable=False)
    ingestion_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    data_freshness = Column(String(20), default="delayed")  # real_time, delayed, end_of_day, estimated
    data_status = Column(String(20), default="valid")  # valid, stale, estimated, unavailable

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_market_price_asset_timestamp", "asset_id", "data_timestamp"),
    )

    asset = relationship("Asset", back_populates="prices")


class MarketCandle(Base):
    """OHLCV candlestick data."""
    __tablename__ = "market_candles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    interval = Column(String(10), nullable=False)  # 1m, 5m, 15m, 1h, 4h, 1d, 1w
    open = Column(Numeric(precision=20, scale=8), nullable=False)
    high = Column(Numeric(precision=20, scale=8), nullable=False)
    low = Column(Numeric(precision=20, scale=8), nullable=False)
    close = Column(Numeric(precision=20, scale=8), nullable=False)
    volume = Column(Numeric(precision=30, scale=8))
    trades = Column(Integer)
    currency = Column(String(10), default="USD")
    timestamp = Column(DateTime(timezone=True), nullable=False)

    provider = Column(String(50), nullable=False)
    ingestion_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("asset_id", "interval", "timestamp", name="uq_candle"),
        Index("ix_candle_asset_interval_ts", "asset_id", "interval", "timestamp"),
    )

    asset = relationship("Asset", back_populates="candles")


class MarketSnapshot(Base):
    """Periodic market-wide snapshot for dashboard."""
    __tablename__ = "market_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    snapshot_type = Column(String(50), nullable=False)  # global, stock_id, crypto, index
    data = Column(JSONB, nullable=False)
    provider = Column(String(50))
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_snapshot_type_ts", "snapshot_type", "timestamp"),
    )


class Fundamental(Base):
    """Company fundamental data."""
    __tablename__ = "fundamentals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    period = Column(String(20))  # Q1_2024, FY2024, TTM
    revenue = Column(Numeric(precision=30, scale=2))
    net_income = Column(Numeric(precision=30, scale=2))
    eps = Column(Float)
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    ps_ratio = Column(Float)
    debt_to_equity = Column(Float)
    current_ratio = Column(Float)
    roe = Column(Float)
    roa = Column(Float)
    profit_margin = Column(Float)
    revenue_growth_yoy = Column(Float)
    earnings_growth_yoy = Column(Float)
    dividend_yield = Column(Float)
    free_cash_flow = Column(Numeric(precision=30, scale=2))
    market_cap = Column(Numeric(precision=30, scale=2))
    enterprise_value = Column(Numeric(precision=30, scale=2))
    beta = Column(Float)

    provider = Column(String(50), nullable=False)
    data_timestamp = Column(DateTime(timezone=True))
    ingestion_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    asset = relationship("Asset", back_populates="fundamentals")


class TechnicalIndicator(Base):
    """Computed technical indicators."""
    __tablename__ = "technical_indicators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    interval = Column(String(10), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    # Trend
    sma_20 = Column(Float)
    sma_50 = Column(Float)
    sma_200 = Column(Float)
    ema_12 = Column(Float)
    ema_26 = Column(Float)

    # Momentum
    rsi_14 = Column(Float)
    macd = Column(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)
    stoch_k = Column(Float)
    stoch_d = Column(Float)

    # Volatility
    bb_upper = Column(Float)
    bb_middle = Column(Float)
    bb_lower = Column(Float)
    atr_14 = Column(Float)

    # Volume
    obv = Column(Float)
    vwap = Column(Float)

    # Trend Strength
    adx = Column(Float)
    plus_di = Column(Float)
    minus_di = Column(Float)

    # Support & Resistance
    support_1 = Column(Float)
    resistance_1 = Column(Float)
    pivot = Column(Float)

    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("asset_id", "interval", "timestamp", name="uq_technical"),
        Index("ix_tech_asset_interval_ts", "asset_id", "interval", "timestamp"),
    )


class OnchainMetric(Base):
    """Cryptocurrency on-chain metrics."""
    __tablename__ = "onchain_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    active_addresses = Column(Integer)
    transaction_count = Column(Integer)
    transaction_volume = Column(Numeric(precision=30, scale=8))
    hash_rate = Column(Numeric(precision=30, scale=2))
    tvl = Column(Numeric(precision=30, scale=2))
    staking_ratio = Column(Float)
    exchange_inflow = Column(Numeric(precision=30, scale=8))
    exchange_outflow = Column(Numeric(precision=30, scale=8))
    whale_transactions = Column(Integer)
    holder_count = Column(Integer)
    top_holder_pct = Column(Float)
    protocol_revenue = Column(Numeric(precision=30, scale=2))
    developer_activity = Column(Float)

    provider = Column(String(50))
    ingestion_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_onchain_asset_ts", "asset_id", "timestamp"),
    )


class DerivativesMetric(Base):
    """Derivatives market data."""
    __tablename__ = "derivatives_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    open_interest = Column(Numeric(precision=30, scale=2))
    funding_rate = Column(Float)
    long_short_ratio = Column(Float)
    liquidations_long = Column(Numeric(precision=30, scale=2))
    liquidations_short = Column(Numeric(precision=30, scale=2))
    volume_24h = Column(Numeric(precision=30, scale=2))

    provider = Column(String(50))
    ingestion_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_deriv_asset_ts", "asset_id", "timestamp"),
    )
