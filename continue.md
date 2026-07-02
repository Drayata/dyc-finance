# MarketPulse AI — Continuation Guide

> **Last updated:** 2026-07-03
> **Status:** MVP Phase 4 partially complete — Backend core done, Frontend core pages done, infrastructure and documentation pending.

---

## ✅ What Has Been Completed

### Infrastructure
- [x] `docker-compose.yml` — PostgreSQL+TimescaleDB, Redis, Backend, Celery Worker/Beat, Frontend
- [x] `.env.example` — All environment variables documented, no secrets
- [x] `.gitignore` — Python, Node, Docker, IDE, model artifacts
- [x] `backend/Dockerfile` — Python 3.12 with PostgreSQL libs
- [x] `frontend/Dockerfile.dev` — Node 20 dev container
- [x] `backend/requirements.txt` — All Python dependencies pinned

### Backend — Database Models (40+ tables)
- [x] `backend/app/models/auth.py` — User, Role, UserSession, Subscription
- [x] `backend/app/models/market.py` — Asset, Exchange, AssetPair, MarketPrice, MarketCandle, MarketSnapshot, Fundamental, TechnicalIndicator, OnchainMetric, DerivativesMetric
- [x] `backend/app/models/news.py` — NewsSource, NewsArticle, NewsEntity, NewsAssetRelation, Event, EventImpact, SentimentResult
- [x] `backend/app/models/signals.py` — Signal, SignalComponent, SignalExplanation, SignalOutcome
- [x] `backend/app/models/ml.py` — ModelVersion, ModelMetric, BacktestRun, BacktestResult
- [x] `backend/app/models/user_features.py` — Watchlist, WatchlistItem, AlertRule, AlertEvent, Notification
- [x] `backend/app/models/ops.py` — DataProvider, ProviderHealth, IngestionJob, DataQualityLog, AuditLog

### Backend — Core Application
- [x] `backend/app/config.py` — Pydantic settings from env vars
- [x] `backend/app/database.py` — Async SQLAlchemy engine + session factory
- [x] `backend/app/main.py` — FastAPI app with CORS, security headers, request ID, error handling
- [x] `backend/app/security/__init__.py` — JWT auth, bcrypt hashing, RBAC, password validation
- [x] `backend/app/schemas/__init__.py` — Pydantic schemas for all endpoints

### Backend — API Routes
- [x] `backend/app/api/auth.py` — Register, login, logout, refresh, forgot-password, profile
- [x] `backend/app/api/markets.py` — Market overview, movers, asset list/detail/candles/indicators/fundamentals/onchain
- [x] `backend/app/api/news.py` — News list, high-impact, categories, per-asset news
- [x] `backend/app/api/signals.py` — Signal list, strongest bullish/bearish, per-asset signal
- [x] `backend/app/api/watchlists.py` — CRUD with ownership checks
- [x] `backend/app/api/alerts.py` — CRUD with limits

### Backend — Providers
- [x] `backend/app/providers/base.py` — Abstract interfaces: MarketDataProvider, NewsProvider, FundamentalProvider, OnchainProvider
- [x] `backend/app/providers/mock_provider.py` — Full demo mode with ID stocks, US stocks, crypto, indices, 8 realistic news articles, fundamentals, on-chain data

### Backend — Analytics Engine
- [x] `backend/app/analytics/technical.py` — SMA, EMA, RSI, MACD, Bollinger Bands, ATR, ADX, support/resistance, composite technical score
- [x] `backend/app/analytics/signal_engine.py` — Hybrid scoring with configurable weights, confidence, risk, expected range, bull/bear factors, invalidation conditions, disclaimers

### Backend — Background Tasks
- [x] `backend/app/tasks/__init__.py` — Celery config with beat schedule
- [x] `backend/app/tasks/market_tasks.py`, `news_tasks.py`, `signal_tasks.py` — Task stubs with retry logic

### Backend — Tests
- [x] `backend/tests/test_core.py` — 20+ tests: technical indicators, signal compliance, mock provider labeling, JWT auth, password hashing, data quality rules

### Frontend — Core
- [x] Next.js 14 App Router + TypeScript + Tailwind CSS
- [x] `frontend/src/types/index.ts` — Full TypeScript types
- [x] `frontend/src/lib/api.ts` — Centralized API client
- [x] `frontend/src/app/globals.css` — Dark/light theme, signal badges, glassmorphism, skeleton loading
- [x] `frontend/src/app/layout.tsx` — Root layout with SEO, dark theme, demo banner

### Frontend — Pages
- [x] Dashboard (`page.tsx`) — Sidebar nav, indices, crypto, signals, news, movers
- [x] Asset Detail (`asset/[symbol]/page.tsx`) — 4 tabs: overview, technical, news, signal
- [x] Signal Center (`signals/page.tsx`) — Direction/type filters, signal cards
- [x] Asset Screener (`assets/page.tsx`) — Search, type filter, sort, pagination
- [x] News Intelligence (`news/page.tsx`) — Category/direction/verification filters, impact pathways

---

## 🔧 What Needs to Be Continued

---

### PRIORITY 1: Make It Run (Critical — Do First)

#### 1.1 — Create Next.js Configuration
**File:** `frontend/next.config.mjs`
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/:path*`,
      },
    ];
  },
};
export default nextConfig;
```

#### 1.2 — Initialize Alembic Database Migrations
```bash
cd backend
alembic init migrations
```
Then edit:
- `alembic.ini` — set `sqlalchemy.url`
- `migrations/env.py` — import all models, set `target_metadata = Base.metadata`
- Generate initial migration: `alembic revision --autogenerate -m "Initial schema"`
- Apply: `alembic upgrade head`

#### 1.3 — Database Seed Script
**File:** `backend/scripts/seed_demo.py`
- Populate exchanges (IDX, NYSE, NASDAQ, Binance)
- Insert demo assets from mock_provider data
- Insert demo news sources
- Insert initial model version record
- Insert data provider records

#### 1.4 — Run Backend Tests & Fix
```bash
cd backend
pip install -r requirements.txt
pytest -v tests/test_core.py
```

#### 1.5 — Docker Compose End-to-End Test
```bash
docker-compose up --build -d
docker-compose ps
curl http://localhost:8000/health
curl http://localhost:3000
```

---

### PRIORITY 2: Missing Frontend Pages (High)

#### 2.1 — Authentication Pages
- `frontend/src/app/login/page.tsx` — Login form with email/password
- `frontend/src/app/register/page.tsx` — Registration form with validation
- `frontend/src/app/forgot-password/page.tsx` — Password reset request

#### 2.2 — Landing Page
- `frontend/src/app/landing/page.tsx` — Public page with hero, features, disclaimer, CTA
- Split `page.tsx` logic: unauthenticated → landing, authenticated → dashboard

#### 2.3 — Watchlist Page
- `frontend/src/app/watchlists/page.tsx` — Create/manage watchlists, add/remove assets

#### 2.4 — Alert Management Page
- `frontend/src/app/alerts/page.tsx` — Create/edit/delete alerts, history

#### 2.5 — User Profile & Settings
- `frontend/src/app/settings/page.tsx` — Theme toggle, mode toggle, timezone
- `frontend/src/app/profile/page.tsx` — User info, subscription

#### 2.6 — Admin Pages
- `frontend/src/app/admin/page.tsx` — Admin dashboard
- `frontend/src/app/admin/providers/page.tsx` — Provider health
- `frontend/src/app/admin/jobs/page.tsx` — Background job monitoring
- `frontend/src/app/admin/data-quality/page.tsx` — Quality logs
- `frontend/src/app/admin/models/page.tsx` — Model monitoring

#### 2.7 — Legal Pages
- `frontend/src/app/disclaimer/page.tsx` — Full disclaimer
- `frontend/src/app/privacy/page.tsx` — Privacy policy
- `frontend/src/app/terms/page.tsx` — Terms and conditions

#### 2.8 — Backtesting Dashboard
- `frontend/src/app/backtests/page.tsx` — Run backtests, view results, compare benchmarks

#### 2.9 — Model Transparency
- `frontend/src/app/model-transparency/page.tsx` — Model card, version history, weights, metrics

#### 2.10 — Extract Shared Sidebar Layout
- `frontend/src/app/(dashboard)/layout.tsx` — Shared layout with sidebar for all dashboard pages
- Move sidebar from `page.tsx` into a reusable layout component

---

### PRIORITY 3: Backend Feature Gaps (High)

#### 3.1 — Backtesting Module
**File:** `backend/app/analytics/backtesting.py`
- Walk-forward validation
- Look-ahead bias prevention
- Transaction cost + slippage modeling
- All metrics: return, hit rate, Sharpe, Sortino, max drawdown, Brier score, etc.
- Benchmark comparison (buy & hold, MA crossover, random)

#### 3.2 — Full 10-Stage News Pipeline
**File:** `backend/app/analytics/news_pipeline.py`
1. Ingestion from sources
2. Deduplication (content hash + semantic similarity)
3. Entity Recognition (spaCy NER)
4. Event Classification
5. Relevance Scoring (0-100)
6. Sentiment Scoring (-1 to +1, per headline/body/entity)
7. Event Impact Scoring (0-100)
8. Direction Classification
9. Time Horizon estimation
10. Explanation Generation (structured evidence only)

#### 3.3 — Production Providers
- `backend/app/providers/alpha_vantage.py` — Stock data adapter
- `backend/app/providers/coingecko.py` — Crypto data adapter
- `backend/app/providers/newsapi.py` — News adapter
- Each implements base interface, handles rate limits, falls back to mock

#### 3.4 — Provider Registry
- `backend/app/providers/registry.py` — Factory selecting mock vs production, auto-fallback

#### 3.5 — Admin API Routes
- `backend/app/api/admin.py` — Provider health, jobs, data quality, models (admin role required)

#### 3.6 — Backtest API Routes
- `backend/app/api/backtests.py` — POST /backtests, GET /backtests/{id}, GET /backtests/{id}/results

#### 3.7 — Email Service
- `backend/app/services/email_service.py` — Password reset, alert notifications via SMTP

#### 3.8 — Rate Limiting Middleware
- `backend/app/security/rate_limiter.py` — Redis-based per-user/per-IP rate limiting

#### 3.9 — Audit Logging
- `backend/app/services/audit_service.py` — Log signal generation, auth events, admin actions

#### 3.10 — WebSocket for Real-Time Prices
- Add `@app.websocket("/ws/prices")` endpoint to `main.py`

---

### PRIORITY 4: Charting (Medium)

#### 4.1 — Install TradingView Lightweight Charts
```bash
cd frontend && npm install lightweight-charts@4
```

#### 4.2 — Chart Components
- `frontend/src/components/charts/CandlestickChart.tsx` — OHLCV candlestick with timeframe selector
- `frontend/src/components/charts/RSIChart.tsx` — RSI oscillator
- `frontend/src/components/charts/MACDChart.tsx` — MACD indicator
- `frontend/src/components/charts/VolumeChart.tsx` — Volume profile
- `frontend/src/components/charts/SentimentChart.tsx` — Sentiment history
- Integrate charts into Asset Detail page

---

### PRIORITY 5: Simple/Advanced Mode (Medium)

#### 5.1 — Mode Context
- `frontend/src/context/UserPreferences.tsx` — React context for mode, theme, timezone
- Persist to localStorage, sync with backend on auth

#### 5.2 — Simple Mode Views
- Signal: direction + confidence + short explanation + risks + time horizon
- Hide: technicals, SHAP, model version, raw data

#### 5.3 — Advanced Mode Views
- Show everything: full indicators, feature contributions, backtest data, model metadata

---

### PRIORITY 6: Testing (High — Do Alongside Development)

#### 6.1 — Run Existing Backend Tests
```bash
cd backend && pytest -v --tb=short
```

#### 6.2 — API Integration Tests
- `backend/tests/test_api.py` — httpx AsyncClient tests for all endpoints

#### 6.3 — Frontend Build
```bash
cd frontend && npm run build
```

#### 6.4 — Signal Compliance Tests
- `backend/tests/test_compliance.py` — No forbidden language, disclaimers present, data sources listed

#### 6.5 — Data Quality Tests
- `backend/tests/test_data_quality.py` — Provider labels, timestamps, source tracking

---

### PRIORITY 7: Documentation (Medium)

| File | Content |
|------|---------|
| `README.md` | Project overview, architecture, quick start, API docs link |
| `DEVELOPMENT.md` | Local dev setup, running tests, code style |
| `DEPLOYMENT.md` | Staging/production deployment, migrations, backups, rollback |
| `SECURITY.md` | Auth architecture, password policy, headers, audit logging |
| `DATA_SOURCES.md` | Provider list, licensing, freshness, attribution |
| `MODEL_CARD.md` | Model type, features, weights, limitations, ethics |
| `docs/erd.md` | Mermaid ER diagram of all 40+ tables |

---

### PRIORITY 8: Production Hardening (Lower for MVP)

- `.github/workflows/ci.yml` — CI/CD with lint, test, build, security scan
- Structured JSON logging with structlog
- Error tracking (Sentry integration)
- Database connection pooling tuning
- Redis cache layer for hot data
- `Makefile` for common commands

---

### PRIORITY 9: Post-MVP Roadmap

| Feature | Complexity |
|---------|------------|
| OAuth/Social Login (Google, GitHub) | Medium |
| Two-Factor Auth (TOTP) | Medium |
| Telegram Bot Notifications | Medium |
| Email Alert Delivery | Medium |
| Economic Calendar Page | Medium |
| Subscription/Payments (Stripe) | High |
| ML Model Training (XGBoost/LightGBM) | High |
| SHAP Feature Attribution | High |
| FinBERT Sentiment Analysis | High |
| spaCy NER Pipeline | Medium |
| LLM Explanation Generation | High |
| PWA Support | Medium |
| Multi-language (Bahasa Indonesia + English) | Medium |
| Data Export (CSV/JSON) | Low |
| API Key Management | Medium |
| Webhook Alerts | Low |
| WhatsApp Integration | High |
| Correlation Matrix | Medium |
| Sector Heatmap | Medium |
| Real-Time WebSocket Feed | High |

---

## ⚠️ Known Issues & Limitations

1. **No `next.config.mjs`** — needs to be created for API rewrites and build
2. **Alembic not initialized** — tables only created via `init_db()` (dev mode only)
3. **Tests written but not executed** — need to run and fix failures
4. **No charting library installed** — `lightweight-charts` needs `npm install`
5. **Simple/Advanced mode** not implemented — all pages show advanced view
6. **Auth pages missing** — no login/register UI
7. **Sidebar only on dashboard** — needs to be extracted to shared layout
8. **No API proxy configured** — frontend calls backend directly
9. **Celery tasks are stubs** — log messages only in demo mode
10. **No production providers** — only mock providers
11. **No email service** — password reset returns success but doesn't send email
12. **No WebSocket** — no real-time price streaming
13. **No Makefile** — common commands not automated
14. **GeistVF font files** may cause 404 (layout references removed but files may still exist)
15. **Tailwind CSS v4** was installed by create-next-app (uses `@import "tailwindcss"` syntax) — globals.css uses this correctly
