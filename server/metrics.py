import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge


# Prometheus metrics
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    labelnames=("method", "path", "status_code"),
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    labelnames=("method", "path", "status_code"),
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
        10.0,
    ),
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress", "HTTP requests in progress", labelnames=("method", "path")
)


def _get_path_template(request: Request) -> str:
    # Prefer route path template to limit cardinality
    route = request.scope.get("route")
    if getattr(route, "path", None):
        return route.path  # type: ignore[attr-defined]
    return request.url.path


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        method = request.method
        path = _get_path_template(request)
        start = time.perf_counter()
        HTTP_REQUESTS_IN_PROGRESS.labels(method=method, path=path).inc()
        status_code = "500"
        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            return response
        finally:
            elapsed = time.perf_counter() - start
            HTTP_REQUESTS_TOTAL.labels(method=method, path=path, status_code=status_code).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=method, path=path, status_code=status_code
            ).observe(elapsed)
            HTTP_REQUESTS_IN_PROGRESS.labels(method=method, path=path).dec()


def instrument_app(app) -> None:
    app.add_middleware(PrometheusMiddleware)


