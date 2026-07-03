"""
MarketPulse AI — FastAPI Application Entry Point
Combines all routers, middleware, and startup/shutdown events.
"""
import time
import uuid
from datetime import datetime, timezone
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import init_db
from app.api import auth, markets, news, signals, watchlists, alerts, backtests

settings = get_settings()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Starting MarketPulse AI", version=settings.APP_VERSION, demo_mode=settings.DEMO_MODE)

    # Initialize database tables (dev only; use Alembic in production)
    if settings.DEBUG or settings.DEMO_MODE:
        await init_db()
        logger.info("Database tables initialized")

    yield

    logger.info("Shutting down MarketPulse AI")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AI-powered market intelligence platform for stocks and cryptocurrencies. "
        "All signals are probabilistic and for educational/analytical purposes only."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request ID Middleware ---
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time"] = f"{duration:.3f}s"

    if duration > 5.0:
        logger.warning("Slow request", path=request.url.path, duration=duration, request_id=request_id)

    return response


# --- Security Headers Middleware ---
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


# --- Register Routers ---
app.include_router(auth.router)
app.include_router(markets.router)
app.include_router(news.router)
app.include_router(signals.router)
app.include_router(watchlists.router)
app.include_router(alerts.router)
app.include_router(backtests.router)


# --- WebSockets ---
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

@app.websocket("/ws/prices")
async def websocket_prices(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # In a real app, this would subscribe to a Redis pub/sub channel
            # For MVP, we just send a mock heartbeat
            await websocket.send_json({"type": "heartbeat", "timestamp": datetime.now(timezone.utc).isoformat()})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info("Client disconnected from price stream")


# --- Health Check ---
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "demo_mode": settings.DEMO_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --- Root ---
@app.get("/", tags=["System"])
async def root():
    """API root with platform information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "demo_mode": settings.DEMO_MODE,
        "docs": "/docs",
        "health": "/health",
        "disclaimer": (
            "The information provided by this platform is intended for educational "
            "and market-analysis purposes only. All signals are probabilistic and "
            "do not guarantee future performance."
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# --- Global Error Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error("Unhandled exception", error=str(exc), request_id=request_id, path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal error occurred. Please try again later.",
            "request_id": request_id,
        },
    )
