"""
MarketPulse AI — Database Seeding Script
Populates the database with required demo data: exchanges, assets, sources, and providers.
"""
import asyncio
import sys
import os
from uuid import uuid4

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session, init_db
from app.models.market import Exchange, Asset
from app.models.ops import DataProvider
from app.models.ml import ModelVersion
from app.providers.mock_provider import MOCK_STOCKS, MOCK_CRYPTO

async def seed_data():
    # Make sure tables exist (using SQLAlchemy create_all for simplicity during seeding local db)
    await init_db()

    async with get_db_session() as session:
        # Check if already seeded
        from sqlalchemy import select
        existing_assets = await session.execute(select(Asset).limit(1))
        if existing_assets.scalar_one_or_none() is not None:
            print("Database already seeded. Skipping.")
            return

        print("Seeding database...")

        # 1. Exchanges
        exchanges = [
            Exchange(id=uuid4(), name="NASDAQ", country="US", timezone="America/New_York", currency="USD", is_active=True),
            Exchange(id=uuid4(), name="NYSE", country="US", timezone="America/New_York", currency="USD", is_active=True),
            Exchange(id=uuid4(), name="IDX", full_name="Indonesia Stock Exchange", country="ID", timezone="Asia/Jakarta", currency="IDR", is_active=True),
            Exchange(id=uuid4(), name="Binance", type="crypto", is_active=True),
            Exchange(id=uuid4(), name="Coinbase", type="crypto", is_active=True),
        ]
        session.add_all(exchanges)

        # 2. Assets (Stocks)
        nyse = next(e for e in exchanges if e.name == "NYSE")
        nasdaq = next(e for e in exchanges if e.name == "NASDAQ")
        idx = next(e for e in exchanges if e.name == "IDX")

        for stock in MOCK_STOCKS:
            exchange = idx if stock.get("country") == "Indonesia" else (nasdaq if stock["symbol"] in ("AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META") else nyse)
            asset = Asset(
                id=uuid4(),
                symbol=stock["symbol"],
                name=stock["name"],
                asset_type="stock",
                exchange_id=exchange.id,
                sector=stock.get("sector"),
                industry=stock.get("industry"),
                country=stock.get("country"),
                is_active=True,
                is_tradable=True,
            )
            session.add(asset)

        # 3. Assets (Crypto)
        binance = next(e for e in exchanges if e.name == "Binance")
        for crypto in MOCK_CRYPTO:
            asset = Asset(
                id=uuid4(),
                symbol=crypto["symbol"],
                name=crypto["name"],
                asset_type="crypto",
                exchange_id=binance.id,
                is_active=True,
                is_tradable=True,
            )
            session.add(asset)

        # 4. Data Providers
        providers = [
            DataProvider(id=uuid4(), name="demo_mock", type="market_data", status="active"),
            DataProvider(id=uuid4(), name="alpha_vantage", type="market_data", status="inactive"),
            DataProvider(id=uuid4(), name="coingecko", type="market_data", status="inactive"),
        ]
        session.add_all(providers)

        # 5. Model Version
        model = ModelVersion(
            id=uuid4(),
            version_tag="v0.1.0",
            model_type="rule_based",
            is_active=True,
            description="Rule-based hybrid scoring model",
            parameters={"weights_stock": {"technical": 0.3, "fundamental": 0.25}, "weights_crypto": {"technical": 0.3, "onchain": 0.25}},
            features_used=["rsi_14", "macd", "sma_20", "sma_50", "sentiment", "impact"],
        )
        session.add(model)

        await session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())
