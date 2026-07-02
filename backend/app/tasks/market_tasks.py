"""
MarketPulse AI — Market Data Tasks
Background tasks for ingesting stock and crypto price data.
"""
import structlog
from app.tasks import celery_app

logger = structlog.get_logger()


@celery_app.task(bind=True, name="app.tasks.market_tasks.ingest_crypto_prices", max_retries=3)
def ingest_crypto_prices(self):
    """Ingest latest cryptocurrency prices from providers."""
    try:
        logger.info("Starting crypto price ingestion")
        # In demo mode, this is a no-op since we use mock data
        # In production, this would call the crypto provider adapter
        logger.info("Crypto price ingestion complete (demo mode: no-op)")
    except Exception as exc:
        logger.error("Crypto price ingestion failed", error=str(exc))
        self.retry(exc=exc)


@celery_app.task(bind=True, name="app.tasks.market_tasks.ingest_stock_prices", max_retries=3)
def ingest_stock_prices(self):
    """Ingest latest stock prices from providers."""
    try:
        logger.info("Starting stock price ingestion")
        logger.info("Stock price ingestion complete (demo mode: no-op)")
    except Exception as exc:
        logger.error("Stock price ingestion failed", error=str(exc))
        self.retry(exc=exc)


@celery_app.task(name="app.tasks.market_tasks.check_provider_health")
def check_provider_health():
    """Check health of all data providers."""
    logger.info("Provider health check complete (demo mode: all healthy)")
