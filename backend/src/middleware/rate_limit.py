import time
from typing import Dict
from collections import defaultdict
from fastapi import Request, HTTPException
from ..config import settings


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)  # IP -> list of request timestamps
        self.window_size = 60  # 60 seconds window
        self.max_requests = 60  # max 60 requests per window

    def is_allowed(self, request: Request) -> bool:
        client_ip = self.get_client_ip(request)
        now = time.time()

        # Clean old requests outside the window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < self.window_size
        ]

        # Check if limit exceeded
        if len(self.requests[client_ip]) >= self.max_requests:
            return False

        # Add current request
        self.requests[client_ip].append(now)
        return True

    def get_client_ip(self, request: Request) -> str:
        # Try to get the real client IP from headers
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()

        # Fallback to client host
        return request.client.host


# Global rate limiter instance
rate_limiter = RateLimiter()