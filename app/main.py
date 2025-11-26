
from fastapi import FastAPI, Request
import time
import random
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title="demo-metrics-app")

# Métricas
REQUEST_COUNT = Counter(
    "demo_requests_total",
    "Total de requests",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "demo_request_latency_seconds",
    "Latencia de request",
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5)
)
BUSINESS_GAUGE = Gauge(
    "demo_business_gauge", "Valor de negocio simulado"
)
ERROR_COUNT = Counter(
    "demo_error_total", "Errores simulados"
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    REQUEST_LATENCY.observe(latency)
    REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
    return response

@app.get("/")
async def root():
    # Simulamos un valor de negocio (ej. colas, backlog, etc.)
    BUSINESS_GAUGE.set(random.randint(0, 100))
    return {"ok": True, "message": "Hello from demo-metrics-app"}

@app.get("/error")
async def make_error():
    ERROR_COUNT.inc()
    return Response(content="simulated error", status_code=500)

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
