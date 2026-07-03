# Deployment Guide

## Architecture Overview
MarketPulse AI requires:
- Next.js Server (Node.js)
- FastAPI Server (Python)
- PostgreSQL Database
- Redis Server (for Rate Limiting and Caching)

## Docker Deployment (Recommended)
The platform includes `Dockerfile` and `docker-compose.yml` (to be added) for simplified orchestration.

1. Configure `.env.production`.
2. Build and run containers:
   ```bash
   docker-compose up -d --build
   ```

## CI/CD Pipeline
- **GitHub Actions**: Automated testing and linting run on every pull request to `main`.
- **Automated Deployments**: Code pushed to `main` is automatically built into Docker images and pushed to a container registry.

## Performance Tuning
- **Database Connection Pooling**: SQLAlchemy is configured with `pool_size=20` and `max_overflow=10` to handle high concurrent traffic.
- **Rate Limiting**: Redis is used to limit API requests to prevent abuse and manage provider API quotas.
