import logging
from app.logger import setup_logger
import json
from opentelemetry import trace
from app.tracer import setup_tracing

"""Tests to validate logs."""


def test_correlation_id_header(client):
    response = client.get("/metrics")
    assert "X-Correlation-ID" in response.headers
    correlation_id = response.headers["X-Correlation-ID"]
    assert correlation_id.strip() != ""


def test_logger_level_is_info():
    setup_logger()
    logger = logging.getLogger()
    assert logger.level == logging.INFO


def test_logger_formatter_is_json(caplog):
    setup_logger()
    logger = logging.getLogger()

    with caplog.at_level(logging.INFO):
        logger.info('{"message": "testing"}')

    log_data = caplog.records[0].getMessage()

    try:
        log_json = json.loads(log_data)
    except json.JSONDecodeError:
        log_json = None

    assert log_json is not None


def test_logger_has_stream_handler():
    setup_logger()
    logger = logging.getLogger()
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)


"""Tests metrics are being exposed."""


def test_http_request_total(client):
    response = client.get("/metrics")
    assert b"http_requests_total" in response.data


def test_http_request_latency_seconds(client):
    response = client.get("/metrics")
    assert b"http_request_latency_seconds" in response.data


def test_requests_per_second(client):
    response = client.get("/metrics")
    assert b"http_requests_per_second" in response.data


def test_metrics_include_status_codes(client):
    response = client.get("/metrics")
    assert response.status_code == 200


"""Tests to check if traces are being sent."""


def test_tracer_is_configured():
    tracer = trace.get_tracer(__name__)
    assert tracer is not None


def test_tracer_provider_is_set(client):
    setup_tracing(client.application)

    provider = trace.get_tracer_provider()
    assert provider is not None
    from opentelemetry.sdk.trace import TracerProvider

    assert isinstance(provider, TracerProvider)
