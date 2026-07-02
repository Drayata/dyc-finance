"""
MarketPulse AI — Celery Task Configuration
Background task processing for market data ingestion, news, and signal recalculation.
"""
from celery import Celery
from celery.schedules import crontab
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "marketpulse",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
    task_default_retry_delay=60,
    task_max_retries=3,
    result_expires=3600,
)

# Scheduled tasks
celery_app.conf.beat_schedule = {
    "ingest-crypto-prices": {
        "task": "app.tasks.market_tasks.ingest_crypto_prices",
        "schedule": 30.0,  # Every 30 seconds
    },
    "ingest-stock-prices": {
        "task": "app.tasks.market_tasks.ingest_stock_prices",
        "schedule": 300.0,  # Every 5 minutes
    },
    "ingest-news": {
        "task": "app.tasks.news_tasks.ingest_news",
        "schedule": 300.0,  # Every 5 minutes
    },
    "recalculate-signals": {
        "task": "app.tasks.signal_tasks.recalculate_all_signals",
        "schedule": 600.0,  # Every 10 minutes
    },
    "health-check-providers": {
        "task": "app.tasks.market_tasks.check_provider_health",
        "schedule": 120.0,  # Every 2 minutes
    },
}


# Import task modules
celery_app.autodiscover_tasks(["app.tasks"])
