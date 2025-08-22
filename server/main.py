from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
from .routes.search import router as search_router

app = FastAPI(title="Reddit MCP Service")


@app.get("/healthz")
async def healthz() -> JSONResponse:
    return JSONResponse({"status": "ok"})


# Note: Metrics are served by the mounted ASGI app at /metrics

# Mount Prometheus metrics ASGI app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Routers
app.include_router(search_router)

