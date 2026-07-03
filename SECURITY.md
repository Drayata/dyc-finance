# Security Policy

## Authentication & Authorization
- All user sessions are managed via JWT (JSON Web Tokens).
- Passwords are cryptographically hashed using `bcrypt` before storage.
- Admin endpoints are protected by Role-Based Access Control (RBAC).

## Secrets Management
- **Never hard-code API keys, database passwords, or JWT secrets.**
- All sensitive configurations must be injected via environment variables.

## Rate Limiting & DoS Prevention
- Global API rate limiting is enforced via Redis.
- Endpoints are limited per IP address or user ID to prevent abuse.

## Cross-Site Scripting (XSS) & CSRF
- Next.js App Router intrinsically protects against XSS in React components.
- CORS policies in FastAPI are strictly bound to permitted frontend origins.

## Vulnerability Reporting
If you discover a security vulnerability within MarketPulse AI, please do not disclose it publicly. Contact the repository administrators immediately.
