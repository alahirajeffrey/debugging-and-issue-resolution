import uuid
from flask import g, request
from opentelemetry import trace


def generate_correlation_id():
    return request.headers.get("X-Correlation-ID", str(uuid.uuid4()))


def correlation_middleware():
    correlation_id = generate_correlation_id()
    g.correlation_id = correlation_id

    # Attach correlation_id to the active span
    span = trace.get_current_span()
    if span and span.is_recording():
        span.set_attribute("correlation_id", correlation_id)
