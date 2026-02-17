"""Secure reference API used by the DevSecOps template."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Callable
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response, status
from pydantic import BaseModel, Field

RATE_LIMIT_REQUESTS = 40
RATE_LIMIT_WINDOW_SECONDS = 60


class EchoRequest(BaseModel):
    message: str = Field(min_length=1, max_length=200)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="DevSecOps Production Template - Reference API",
    description="Reference service with baseline security and delivery standards.",
    version="0.1.0",
    lifespan=lifespan,
)


request_buckets: dict[str, deque[float]] = defaultdict(deque)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next: Callable) -> Response:
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next: Callable) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
    if request.url.path.startswith("/health"):
        return await call_next(request)

    client_host = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = request_buckets[client_host]

    while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_SECONDS:
        bucket.popleft()

    if len(bucket) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Retry later.",
        )

    bucket.append(now)
    return await call_next(request)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/echo")
def echo(payload: EchoRequest) -> dict[str, str]:
    return {"echo": payload.message}
