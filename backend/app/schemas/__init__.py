"""
MarketPulse AI — Pydantic Schemas
Request/response validation for all API endpoints.
"""
from datetime import datetime
from typing import Optional, List, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ==============================================================================
# Auth Schemas
# ==============================================================================

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenRefresh(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: str
    username: str
    full_name: Optional[str]
    role: str
    preferred_mode: str
    preferred_theme: str
    is_verified: bool
    created_at: datetime

class PasswordResetRequest(BaseModel):
    email: EmailStr

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferred_mode: Optional[str] = None
    preferred_theme: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None


# ==============================================================================
# Market Schemas
# ==============================================================================

class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    symbol: str
    name: str
    asset_type: str
    sector: Optional[str]
    industry: Optional[str]
    country: Optional[str]
    currency: Optional[str]
    is_active: bool
    data_quality_score: Optional[float]
    liquidity_tier: Optional[str]
    manipulation_risk: bool
    low_liquidity_warning: bool
    unverified_contract: bool

class AssetDetailResponse(AssetResponse):
    description: Optional[str]
    website: Optional[str]
    blockchain: Optional[str]
    max_supply: Optional[float]
    circulating_supply: Optional[float]
    has_sufficient_history: bool
    latest_price: Optional["MarketPriceResponse"] = None
    latest_signal: Optional["SignalResponse"] = None

class MarketPriceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    price: float
    price_change_24h: Optional[float]
    price_change_pct_24h: Optional[float]
    volume_24h: Optional[float]
    market_cap: Optional[float]
    high_24h: Optional[float]
    low_24h: Optional[float]
    open_24h: Optional[float]
    currency: str
    provider: str
    data_timestamp: datetime
    data_freshness: str
    data_status: str

class CandleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float]

class TechnicalIndicatorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    timestamp: datetime
    interval: str
    sma_20: Optional[float]
    sma_50: Optional[float]
    sma_200: Optional[float]
    ema_12: Optional[float]
    ema_26: Optional[float]
    rsi_14: Optional[float]
    macd: Optional[float]
    macd_signal: Optional[float]
    macd_histogram: Optional[float]
    bb_upper: Optional[float]
    bb_middle: Optional[float]
    bb_lower: Optional[float]
    atr_14: Optional[float]
    adx: Optional[float]
    support_1: Optional[float]
    resistance_1: Optional[float]

class FundamentalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    period: Optional[str]
    revenue: Optional[float]
    net_income: Optional[float]
    eps: Optional[float]
    pe_ratio: Optional[float]
    pb_ratio: Optional[float]
    debt_to_equity: Optional[float]
    roe: Optional[float]
    profit_margin: Optional[float]
    revenue_growth_yoy: Optional[float]
    dividend_yield: Optional[float]
    market_cap: Optional[float]
    provider: str
    data_timestamp: Optional[datetime]

class MarketOverviewResponse(BaseModel):
    timestamp: datetime
    demo_mode: bool
    global_market: dict
    us_market: dict
    id_market: dict
    crypto_market: dict
    top_gainers: List[dict]
    top_losers: List[dict]
    most_active: List[dict]
    high_impact_news: List[dict]
    market_regime: str
    risk_condition: str
    disclaimer: str

class MarketMoversResponse(BaseModel):
    gainers: List[dict]
    losers: List[dict]
    most_active: List[dict]
    unusual_volume: List[dict]
    timestamp: datetime
    demo_mode: bool


# ==============================================================================
# News Schemas
# ==============================================================================

class NewsArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    summary: Optional[str]
    source_name: Optional[str] = None
    published_at: datetime
    relevance_score: Optional[float]
    overall_sentiment: Optional[float]
    impact_score: Optional[float]
    impact_direction: Optional[str]
    impact_time_horizon: Optional[str]
    impact_pathway: Optional[str]
    event_category: Optional[str]
    is_verified: bool
    source_credibility_score: Optional[float]
    related_assets: Optional[List[dict]] = None

class NewsDetailResponse(NewsArticleResponse):
    headline_sentiment: Optional[float]
    body_sentiment: Optional[float]
    uncertainty_score: Optional[float]
    emotional_intensity: Optional[float]
    surprise_factor: Optional[float]
    novelty_score: Optional[float]
    already_priced_in: bool
    event_attributes: Optional[dict]
    entities: Optional[List[dict]] = None
    data_quality_score: Optional[float]


# ==============================================================================
# Signal Schemas
# ==============================================================================

class SignalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    asset_id: UUID
    asset_symbol: Optional[str] = None
    asset_name: Optional[str] = None
    direction: str
    final_score: float
    confidence_score: float
    risk_level: str
    time_horizon: str
    price_at_signal: float
    expected_move_low: Optional[float]
    expected_move_high: Optional[float]

    # Component scores
    technical_score: Optional[float]
    fundamental_score: Optional[float]
    news_score: Optional[float]
    market_context_score: Optional[float]
    onchain_score: Optional[float]
    data_quality_score: Optional[float]
    risk_penalty: Optional[float]

    # Evidence
    bull_factors: Optional[List[dict]]
    bear_factors: Optional[List[dict]]
    key_risks: Optional[List[dict]]
    related_news_ids: Optional[List[UUID]]
    invalidation_conditions: Optional[List[dict]]
    conflicting_signals: Optional[List[dict]]

    # Metadata
    data_sources: Optional[List[str]]
    feature_contributions: Optional[dict]
    weights_used: Optional[dict]
    calculation_timestamp: datetime
    expires_at: Optional[datetime]
    disclaimer: str

class SignalDetailResponse(SignalResponse):
    explanations: Optional[List[dict]] = None
    components: Optional[List[dict]] = None
    outcomes: Optional[List[dict]] = None


# ==============================================================================
# Watchlist Schemas
# ==============================================================================

class WatchlistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None

class WatchlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str]
    is_default: bool
    created_at: datetime
    items: Optional[List["WatchlistItemResponse"]] = None

class WatchlistItemAdd(BaseModel):
    asset_id: UUID
    target_price_high: Optional[float] = None
    target_price_low: Optional[float] = None
    notes: Optional[str] = None

class WatchlistItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    asset_id: UUID
    asset_symbol: Optional[str] = None
    asset_name: Optional[str] = None
    target_price_high: Optional[float]
    target_price_low: Optional[float]
    notes: Optional[str]
    added_at: datetime


# ==============================================================================
# Alert Schemas
# ==============================================================================

class AlertCreate(BaseModel):
    asset_id: UUID
    alert_type: str
    condition: dict
    priority: str = "medium"
    channels: List[str] = ["in_app"]
    cooldown_minutes: int = 60
    is_one_time: bool = False

class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    asset_id: UUID
    alert_type: str
    condition: dict
    priority: str
    channels: Any
    is_active: bool
    last_triggered_at: Optional[datetime]
    trigger_count: int
    created_at: datetime

class AlertUpdate(BaseModel):
    condition: Optional[dict] = None
    priority: Optional[str] = None
    channels: Optional[List[str]] = None
    is_active: Optional[bool] = None


# ==============================================================================
# Backtest Schemas
# ==============================================================================

class BacktestCreate(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    asset_type: str = "stock"
    asset_symbols: Optional[List[str]] = None
    initial_capital: float = 100000.0
    transaction_cost_bps: float = 10.0
    slippage_bps: float = 5.0

class BacktestRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: Optional[str]
    status: str
    start_date: datetime
    end_date: datetime
    asset_type: Optional[str]
    total_return_pct: Optional[float]
    annualized_return_pct: Optional[float]
    max_drawdown_pct: Optional[float]
    sharpe_ratio: Optional[float]
    sortino_ratio: Optional[float]
    hit_rate: Optional[float]
    profit_factor: Optional[float]
    total_trades: Optional[int]
    precision: Optional[float]
    recall: Optional[float]
    f1_score: Optional[float]
    benchmark_return_pct: Optional[float]
    benchmark_name: Optional[str]
    excess_return: Optional[float]
    created_at: datetime


# ==============================================================================
# Common Schemas
# ==============================================================================

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int

class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None
    request_id: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    demo_mode: bool
    database: str
    redis: str
    timestamp: datetime
