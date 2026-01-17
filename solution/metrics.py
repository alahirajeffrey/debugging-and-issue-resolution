from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Response, request
import time

# Existing metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency",
    ["endpoint"],
)

# New metric: requests per second (RPS)
REQUESTS_PER_SECOND = Gauge(
    "http_requests_per_second",
    "HTTP requests per second",
    ["endpoint"],
)

# Store the last count and timestamp for RPS calculation
_LAST_COUNTS = {}
_LAST_TIMES = {}


def setup_metrics(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def record_metrics(response):
        latency = time.time() - request.start_time
        endpoint = request.path
        REQUEST_COUNT.labels(
            request.method, endpoint, response.status_code).inc()
        REQUEST_LATENCY.labels(endpoint).observe(latency)

        # --- Calculate RPS ---
        key = endpoint
        current_count = REQUEST_COUNT.labels(
            request.method, endpoint, response.status_code
        )._value.get()
        now = time.time()

        last_count = _LAST_COUNTS.get(key, 0)
        last_time = _LAST_TIMES.get(key, now)

        delta_count = current_count - last_count
        delta_time = now - last_time

        rps = delta_count / delta_time if delta_time > 0 else 0
        REQUESTS_PER_SECOND.labels(endpoint=endpoint).set(rps)

        # Update last values
        _LAST_COUNTS[key] = current_count
        _LAST_TIMES[key] = now

        return response

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")
