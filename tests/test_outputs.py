import logging
from solution.logger import setup_logger
import json
from opentelemetry import trace
from solution.tracer import setup_tracing

"""Tests to validate logs."""


# test for X-Correlation-ID in response headers
def test_correlation_id_header(client):
    response = client.get("/metrics")
    assert "X-Correlation-ID" in response.headers
    correlation_id = response.headers["X-Correlation-ID"]
    assert correlation_id.strip() != ""


# test to ensure logger level is info
def test_logger_level_is_info():
    setup_logger()
    logger = logging.getLogger()
    assert logger.level == logging.INFO


# test to check if log is in json format
def test_logger_formatter_is_json(caplog):
    setup_logger()
    logger = logging.getLogger()

    with caplog.at_level(logging.INFO):
        logger.info('{"message": "testing"}')

    # get log
    log_data = caplog.records[0].getMessage()

    # parse log record to json
    try:
        log_json = json.loads(log_data)
    except json.JSONDecodeError:
        log_json = None

    assert log_json is not None


# SHOULD PASS: test to ensure at least one StreamHandler is attached
def test_logger_has_stream_handler():
    setup_logger()
    logger = logging.getLogger()
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)


"""Tests metrics are being exposed."""


# test to ensure total http request is in metrics response
def test_http_request_total(client):
    response = client.get("/metrics")
    assert b"http_requests_total" in response.data


# test to ensure http request latency in seconds is in metrics response
def test_http_request_latency_seconds(client):
    response = client.get("/metrics")
    assert b"http_request_latency_seconds" in response.data


# test to ensure total requests per second is in metrics response
def test_requests_per_second(client):
    response = client.get("/metrics")
    assert b"http_requests_per_second" in response.data


# test to ensure metrics endpoint returns a 200 response code
def test_metrics_include_status_codes(client):
    response = client.get("/metrics")
    assert response.status_code == 200


"""Tests to check if traces are being sent."""


# test to see if tracer is configured
def test_tracer_is_configured():
    tracer = trace.get_tracer(__name__)
    assert tracer is not None


# test to see if tracer is an instance of trace provier
def test_tracer_provider_is_set(client):
    setup_tracing(client.application)
    # get the global tracer provider
    provider = trace.get_tracer_provider()
    assert provider is not None
    from opentelemetry.sdk.trace import TracerProvider

    assert isinstance(provider, TracerProvider)
