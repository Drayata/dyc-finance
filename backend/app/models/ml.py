"""
MarketPulse AI — ML & Backtesting Models
Model versioning, performance metrics, backtest runs and results.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base


class ModelVersion(Base):
    """Tracks ML model versions for reproducibility."""
    __tablename__ = "model_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)  # e.g., "stock_signal_v1", "crypto_signal_v1"
    version = Column(String(50), nullable=False)
    model_type = Column(String(50), nullable=False)  # xgboost, rule_based, hybrid
    asset_type = Column(String(20))  # stock, crypto, all
    description = Column(Text)

    # Configuration
    features = Column(JSONB)  # List of features used
    hyperparameters = Column(JSONB)
    weights = Column(JSONB)  # Component weights
    thresholds = Column(JSONB)  # Signal classification thresholds
    training_config = Column(JSONB)

    # Training info
    training_data_start = Column(DateTime(timezone=True))
    training_data_end = Column(DateTime(timezone=True))
    training_samples = Column(Integer)
    validation_samples = Column(Integer)
    test_samples = Column(Integer)

    # Status
    is_active = Column(Boolean, default=False)  # Is this the current production model?
    is_deprecated = Column(Boolean, default=False)
    deployed_at = Column(DateTime(timezone=True))
    retired_at = Column(DateTime(timezone=True))

    # Artifact
    model_artifact_path = Column(String(500))  # Path to saved model file

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    metrics = relationship("ModelMetric", back_populates="model_version", cascade="all, delete-orphan")
    backtest_runs = relationship("BacktestRun", back_populates="model_version", cascade="all, delete-orphan")


class ModelMetric(Base):
    """Performance metrics for a model version (ongoing monitoring)."""
    __tablename__ = "model_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    period = Column(String(20))  # 1d, 7d, 30d, 90d, all
    market_regime = Column(String(50))  # bullish, bearish, sideways, volatile
    asset_type = Column(String(20))
    sample_size = Column(Integer)
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_metric_model_name", "model_version_id", "metric_name"),
    )

    model_version = relationship("ModelVersion", back_populates="metrics")


class BacktestRun(Base):
    """Individual backtest execution."""
    __tablename__ = "backtest_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_version_id = Column(UUID(as_uuid=True), ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255))
    description = Column(Text)

    # Configuration
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    asset_universe = Column(JSONB)  # Assets included
    asset_type = Column(String(20))
    initial_capital = Column(Float, default=100000.0)
    transaction_cost_bps = Column(Float, default=10.0)  # Basis points
    slippage_bps = Column(Float, default=5.0)
    rebalance_frequency = Column(String(20))

    # Validation method
    validation_method = Column(String(50))  # walk_forward, purged_cv, time_split
    train_window_days = Column(Integer)
    test_window_days = Column(Integer)
    gap_days = Column(Integer, default=1)  # Purge gap

    # Status
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Aggregate metrics
    total_return_pct = Column(Float)
    annualized_return_pct = Column(Float)
    max_drawdown_pct = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    hit_rate = Column(Float)
    profit_factor = Column(Float)
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    avg_return_per_trade = Column(Float)
    median_return_per_trade = Column(Float)

    # Advanced metrics
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    roc_auc = Column(Float)
    brier_score = Column(Float)
    calibration_error = Column(Float)
    turnover = Column(Float)

    # Benchmark comparison
    benchmark_return_pct = Column(Float)
    benchmark_name = Column(String(100), default="buy_and_hold")
    excess_return = Column(Float)

    # Full results
    results_summary = Column(JSONB)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    model_version = relationship("ModelVersion", back_populates="backtest_runs")
    results = relationship("BacktestResult", back_populates="backtest_run", cascade="all, delete-orphan")


class BacktestResult(Base):
    """Individual trade/signal result within a backtest."""
    __tablename__ = "backtest_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    backtest_run_id = Column(UUID(as_uuid=True), ForeignKey("backtest_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_symbol = Column(String(50), nullable=False)
    signal_direction = Column(String(20), nullable=False)
    signal_score = Column(Float)
    confidence_score = Column(Float)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    entry_date = Column(DateTime(timezone=True), nullable=False)
    exit_date = Column(DateTime(timezone=True), nullable=False)
    return_pct = Column(Float, nullable=False)
    return_after_costs = Column(Float)
    holding_period_days = Column(Integer)
    was_correct = Column(Boolean)
    market_regime = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("ix_bt_result_run", "backtest_run_id"),
    )

    backtest_run = relationship("BacktestRun", back_populates="results")
