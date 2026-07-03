# Development Guide

## Environment Setup
1. Clone the repository.
2. Refer to the `README.md` for local installation of dependencies.
3. Configure the `.env` file in the `/backend` directory:
   ```env
   # Database
   DATABASE_URL=postgresql://user:password@localhost/marketpulse
   REDIS_URL=redis://localhost:6379/0

   # Security
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # External APIs
   ALPHA_VANTAGE_API_KEY=your_key
   COINGECKO_API_KEY=your_key
   NEWS_API_KEY=your_key
   ```
4. Set up `/frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Branching Strategy
- `main`: Production-ready code.
- `develop`: Staging and active development.
- Feature branches: `feature/your-feature-name`
- Bug fixes: `fix/issue-description`

## Code Style & Linting
- **Frontend**: Follow Next.js conventions. Use `npm run lint` and `npm run format`.
- **Backend**: Follow PEP 8 guidelines. Use `black`, `isort`, and `flake8` for formatting and linting. Type hinting is mandatory for all new FastAPI endpoints.

## Database Migrations
Migrations are handled via Alembic.
To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```
To apply migrations:
```bash
alembic upgrade head
```

## Adding New Data Providers
To add a new data provider (e.g., a new crypto exchange):
1. Create a new adapter in `backend/app/providers/`.
2. Ensure it implements the `MarketDataProvider` base class methods.
3. Register the provider in `backend/app/providers/registry.py`.
