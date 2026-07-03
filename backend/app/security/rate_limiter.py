import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException
from functools import wraps

class SimpleRateLimiter:
    """
    In-memory rate limiter for MVP.
    In a true production environment, this should be backed by Redis
    using a sliding window or token bucket algorithm.
    """
    def __init__(self):
        # Format: { "ip_or_user": (timestamp, count) }
        self.requests: Dict[str, Tuple[float, int]] = {}

    def is_allowed(self, key: str, limit: int, window_seconds: int) -> bool:
        current_time = time.time()
        
        if key in self.requests:
            window_start, count = self.requests[key]
            
            # If the current window has expired, reset
            if current_time - window_start > window_seconds:
                self.requests[key] = (current_time, 1)
                return True
                
            # If within window, check limit
            if count >= limit:
                return False
                
            # Increment count
            self.requests[key] = (window_start, count + 1)
            return True
        else:
            # First request
            self.requests[key] = (current_time, 1)
            return True

# Global instance
rate_limiter = SimpleRateLimiter()

def rate_limit(limit: int, window: int = 60):
    """
    Dependency to rate limit endpoints.
    Usage: @app.get("/api/data", dependencies=[Depends(rate_limit(10, 60))])
    """
    def _rate_limit_dep(request: Request):
        # Use client IP as the key. If authenticated, use user ID.
        # This is a basic implementation for the MVP.
        client_ip = request.client.host if request.client else "unknown"
        
        # Try to get user from state if auth middleware ran
        user = getattr(request.state, "user", None)
        key = f"user:{user.id}" if user else f"ip:{client_ip}"
        
        if not rate_limiter.is_allowed(key, limit, window):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
            
    return _rate_limit_dep
