"""
MarketPulse AI — User Feature Models
Watchlists, alerts, and notifications.
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Text, Integer,
    Float, Enum as SAEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class AlertType(str, enum.Enum):
    PRICE_TARGET = "price_target"
    PRICE_CHANGE = "price_change"
    VOLUME = "volume"
    NEWS = "news"
    SENTIMENT_CHANGE = "sentiment_change"
    SIGNAL_CHANGE = "signal_change"
    RISK_INCREASE = "risk_increase"
    DATA_QUALITY = "data_quality"


class AlertPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationChannel(str, enum.Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    PUSH = "push"
    TELEGRAM = "telegram"


class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="watchlists")
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    watchlist_id = Column(UUID(as_uuid=True), ForeignKey("watchlists.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    target_price_high = Column(Float)
    target_price_low = Column(Float)
    notes = Column(Text)
    sort_order = Column(Integer, default=0)
    added_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    watchlist = relationship("Watchlist", back_populates="items")
    asset = relationship("Asset", back_populates="watchlist_items")


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(SAEnum(AlertType), nullable=False)
    condition = Column(JSONB, nullable=False)  # e.g., {"operator": "gte", "value": 150.0}
    priority = Column(SAEnum(AlertPriority), default=AlertPriority.MEDIUM)
    channels = Column(JSONB, default=["in_app"])  # ["in_app", "email", "telegram"]
    cooldown_minutes = Column(Integer, default=60)
    max_triggers_per_day = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    is_one_time = Column(Boolean, default=False)
    last_triggered_at = Column(DateTime(timezone=True))
    trigger_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="alert_rules")
    events = relationship("AlertEvent", back_populates="alert_rule", cascade="all, delete-orphan")


class AlertEvent(Base):
    """Record of a triggered alert."""
    __tablename__ = "alert_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_rule_id = Column(UUID(as_uuid=True), ForeignKey("alert_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    triggered_value = Column(Float)
    message = Column(Text, nullable=False)
    priority = Column(SAEnum(AlertPriority))
    delivery_status = Column(JSONB)  # {"in_app": "delivered", "email": "sent"}
    triggered_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    alert_rule = relationship("AlertRule", back_populates="events")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50))  # alert, signal, system, news
    priority = Column(SAEnum(AlertPriority), default=AlertPriority.MEDIUM)
    channel = Column(SAEnum(NotificationChannel), default=NotificationChannel.IN_APP)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True))
    data = Column(JSONB)  # Additional context (asset_id, signal_id, etc.)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_notification_user_read", "user_id", "is_read"),
    )

    user = relationship("User", back_populates="notifications")
