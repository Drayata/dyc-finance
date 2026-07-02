"""
MarketPulse AI — Signal & Recommendation Models
Signal generation with full explainability and outcome tracking.
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Text, Integer,
    Float, Enum as SAEnum, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base


class SignalDirection(str, enum.Enum):
    STRONG_BULLISH = "strong_bullish"
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"
    STRONG_BEARISH = "strong_bearish"


class RiskLevel(str, enum.Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class Signal(Base):
    """Primary signal record for an asset."""
    __tablename__ = "signals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("model_versions.id"), index=True)

    # Signal output
    direction = Column(SAEnum(SignalDirection), nullable=False)
    final_score = Column(Float, nullable=False)  # -100 to +100
    confidence_score = Column(Float, nullable=False)  # 0 to 100
    risk_level = Column(SAEnum(RiskLevel), nullable=False)
    time_horizon = Column(String(20), nullable=False)  # immediate, short_term, swing, medium_term

    # Price context
    price_at_signal = Column(Float, nullable=False)
    expected_move_low = Column(Float)   # Expected % move (lower bound)
    expected_move_high = Column(Float)  # Expected % move (upper bound)

    # Component scores (for transparency)
    technical_score = Column(Float)
    fundamental_score = Column(Float)
    news_score = Column(Float)
    market_context_score = Column(Float)
    onchain_score = Column(Float)
    derivatives_score = Column(Float)
    liquidity_score = Column(Float)
    data_quality_score = Column(Float)
    risk_penalty = Column(Float)

    # Supporting evidence
    bull_factors = Column(JSONB)   # Top 3 bullish factors
    bear_factors = Column(JSONB)   # Top 3 bearish factors
    neutral_factors = Column(JSONB)
    key_risks = Column(JSONB)      # Top 3 risks
    related_news_ids = Column(ARRAY(UUID(as_uuid=True)))

    # Invalidation
    invalidation_conditions = Column(JSONB)  # e.g., [{"condition": "price drops below 150", "type": "price"}]
    expires_at = Column(DateTime(timezone=True))

    # Metadata
    is_active = Column(Boolean, default=True)
    data_sources = Column(ARRAY(String))
    feature_contributions = Column(JSONB)  # SHAP values or similar
    conflicting_signals = Column(JSONB)    # Evidence that contradicts the signal
    calculation_timestamp = Column(DateTime(timezone=True), nullable=False)
    config_version = Column(String(50))
    weights_used = Column(JSONB)  # The exact weights used for this signal

    # Disclaimer
    disclaimer = Column(Text, default=(
        "This analytical signal is for educational and market-analysis purposes only. "
        "It does not constitute personalized investment advice. "
        "All signals are probabilistic and do not guarantee future performance."
    ))

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_signal_asset_active", "asset_id", "is_active"),
        Index("ix_signal_direction", "direction"),
        Index("ix_signal_created", "created_at"),
    )

    asset = relationship("Asset", back_populates="signals")
    components = relationship("SignalComponent", back_populates="signal", cascade="all, delete-orphan")
    explanations = relationship("SignalExplanation", back_populates="signal", cascade="all, delete-orphan")
    outcomes = relationship("SignalOutcome", back_populates="signal", cascade="all, delete-orphan")


class SignalComponent(Base):
    """Individual component scores that make up the final signal."""
    __tablename__ = "signal_components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True), ForeignKey("signals.id", ondelete="CASCADE"), nullable=False, index=True)
    component_name = Column(String(50), nullable=False)  # technical, fundamental, news, etc.
    raw_score = Column(Float, nullable=False)
    weighted_score = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    sub_scores = Column(JSONB)  # Breakdown: {"rsi": 65, "macd": 40, ...}
    data_quality = Column(Float, default=50.0)
    data_sources = Column(ARRAY(String))
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    signal = relationship("Signal", back_populates="components")


class SignalExplanation(Base):
    """LLM-generated and system-generated explanations for signals."""
    __tablename__ = "signal_explanations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True), ForeignKey("signals.id", ondelete="CASCADE"), nullable=False, index=True)
    explanation_type = Column(String(20), nullable=False)  # fact, calculation, interpretation
    category = Column(String(50))  # bull_case, bear_case, neutral_case, summary
    content = Column(Text, nullable=False)
    evidence = Column(JSONB)  # Facts backing this explanation
    source_type = Column(String(20))  # system, llm
    data_timestamps = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    signal = relationship("Signal", back_populates="explanations")


class SignalOutcome(Base):
    """Tracks actual outcomes after signal generation for validation."""
    __tablename__ = "signal_outcomes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True), ForeignKey("signals.id", ondelete="CASCADE"), nullable=False, index=True)
    evaluation_period = Column(String(20), nullable=False)  # 1d, 7d, 30d
    price_at_evaluation = Column(Float, nullable=False)
    actual_return_pct = Column(Float, nullable=False)
    was_direction_correct = Column(Boolean)
    was_within_range = Column(Boolean)
    invalidated = Column(Boolean, default=False)
    invalidation_reason = Column(Text)
    evaluated_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    signal = relationship("Signal", back_populates="outcomes")
