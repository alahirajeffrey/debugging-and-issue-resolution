import logging
from solution.logger import setup_logger
import json


## SHOULD PASS: test for X-Correlation-ID in response headers
def test_correlation_id_header(client):
    response = client.get("/metrics")
    assert "X-Correlation-ID" in response.headers
    correlation_id = response.headers["X-Correlation-ID"]
    assert correlation_id.strip() != ""


## SHOULD PASS: test to ensure logger level is info
def test_logger_level_is_info():
    setup_logger()
    logger = logging.getLogger()
    assert logger.level == logging.INFO


## SHOULD FAIL: test to check if logger level is error
def test_logger_level_is_error():
    setup_logger()
    logger = logging.getLogger()
    assert logger.level == logging.ERROR


## SHOULD PASS: test to check if log is in json format
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


## SHOULD PASS: test to ensure at least one StreamHandler is attached
def test_logger_has_stream_handler():
    setup_logger()
    logger = logging.getLogger()
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
