"""
MarketPulse AI — Operations & Monitoring Models
Provider health, data quality, ingestion jobs, and audit logs.
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Text, Integer,
    Float, Enum as SAEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base


class ProviderStatus(str, enum.Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    RATE_LIMITED = "rate_limited"
    MAINTENANCE = "maintenance"


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    DEAD_LETTER = "dead_letter"
    CANCELLED = "cancelled"


class DataProvider(Base):
    __tablename__ = "data_providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    provider_type = Column(String(50), nullable=False)  # stock, crypto, news, fundamental, onchain
    base_url = Column(String(500))
    api_version = Column(String(20))
    status = Column(SAEnum(ProviderStatus), default=ProviderStatus.HEALTHY)
    is_primary = Column(Boolean, default=False)
    is_fallback = Column(Boolean, default=False)
    rate_limit_per_minute = Column(Integer, default=60)
    rate_limit_remaining = Column(Integer)
    rate_limit_reset_at = Column(DateTime(timezone=True))
    license_type = Column(String(50))  # free, basic, pro, enterprise
    license_restrictions = Column(Text)
    supports_realtime = Column(Boolean, default=False)
    data_delay_seconds = Column(Integer, default=0)
    last_success_at = Column(DateTime(timezone=True))
    last_failure_at = Column(DateTime(timezone=True))
    consecutive_failures = Column(Integer, default=0)
    uptime_pct_30d = Column(Float, default=100.0)
    is_active = Column(Boolean, default=True)
    config = Column(JSONB)  # Provider-specific config (not secrets)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    health_records = relationship("ProviderHealth", back_populates="provider", cascade="all, delete-orphan")


class ProviderHealth(Base):
    """Point-in-time health check records."""
    __tablename__ = "provider_health"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("data_providers.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(SAEnum(ProviderStatus), nullable=False)
    response_time_ms = Column(Integer)
    error_message = Column(Text)
    error_code = Column(String(50))
    checked_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_provider_health_ts", "provider_id", "checked_at"),
    )

    provider = relationship("DataProvider", back_populates="health_records")


class IngestionJob(Base):
    """Background data ingestion job tracking."""
    __tablename__ = "ingestion_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type = Column(String(50), nullable=False)  # market_data, news, fundamentals, onchain, signals
    provider_name = Column(String(100))
    asset_symbol = Column(String(50))
    status = Column(SAEnum(JobStatus), default=JobStatus.PENDING)
    celery_task_id = Column(String(255), index=True)
    priority = Column(Integer, default=5)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    error_message = Column(Text)
    error_traceback = Column(Text)
    records_processed = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    metadata = Column(JSONB)
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    is_idempotent = Column(Boolean, default=True)
    idempotency_key = Column(String(255), unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_job_status", "status"),
        Index("ix_job_type_status", "job_type", "status"),
    )


class DataQualityLog(Base):
    """Data quality checks and warnings."""
    __tablename__ = "data_quality_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="SET NULL"), index=True)
    provider_name = Column(String(100))
    check_type = Column(String(50), nullable=False)  # price_consistency, freshness, completeness, anomaly
    severity = Column(String(20), nullable=False)  # info, warning, error, critical
    message = Column(Text, nullable=False)
    details = Column(JSONB)
    quality_score = Column(Float)  # 0-100
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_dq_severity", "severity"),
        Index("ix_dq_asset", "asset_id"),
    )


class AuditLog(Base):
    """Audit trail for important actions."""
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))  # signal, model, user, provider
    resource_id = Column(String(255))
    details = Column(JSONB)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_audit_action", "action"),
        Index("ix_audit_user", "user_id"),
        Index("ix_audit_created", "created_at"),
    )
