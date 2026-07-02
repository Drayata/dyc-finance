"""
MarketPulse AI — News Ingestion Tasks
"""
import structlog
from app.tasks import celery_app

logger = structlog.get_logger()


@celery_app.task(bind=True, name="app.tasks.news_tasks.ingest_news", max_retries=3)
def ingest_news(self):
    """Ingest and process news from all active sources."""
    try:
        logger.info("Starting news ingestion")
        logger.info("News ingestion complete (demo mode: no-op)")
    except Exception as exc:
        logger.error("News ingestion failed", error=str(exc))
        self.retry(exc=exc)
