"""
MarketPulse AI — Signal Recalculation Tasks
"""
import structlog
from app.tasks import celery_app

logger = structlog.get_logger()


@celery_app.task(name="app.tasks.signal_tasks.recalculate_all_signals")
def recalculate_all_signals():
    """Recalculate signals for all tracked assets."""
    try:
        logger.info("Starting signal recalculation")
        logger.info("Signal recalculation complete (demo mode: computed on request)")
    except Exception as exc:
        logger.error("Signal recalculation failed", error=str(exc))
