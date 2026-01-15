import logging
from flask import g, has_request_context
from pythonjsonlogger import jsonlogger
from opentelemetry.trace import get_current_span


class CorrelationIdFilter(logging.Filter):
    """
    Inject correlation_id, trace_id, and span_id into every log record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        ## Only inject if inside a Flask request
        if has_request_context():
            record.correlation_id = getattr(g, "correlation_id", None)
        else:
            record.correlation_id = None

        # add trace_id and span_id from OpenTelemetry
        span = get_current_span()
        if span:
            ctx = span.get_span_context()
            record.trace_id = format(ctx.trace_id, "032x") if ctx.trace_id != 0 else None
            record.span_id = format(ctx.span_id, "016x") if ctx.span_id != 0 else None
        else:
            record.trace_id = None
            record.span_id = None

        return True


def setup_logger():
    """
    Setup JSON logging for the application, injecting correlation IDs and trace info.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ## prevent duplicate handlers 
    if logger.handlers:
        return

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s %(trace_id)s %(span_id)s"
    )
    handler.setFormatter(formatter)

    ## attach filter to inject observability fields
    handler.addFilter(CorrelationIdFilter())

    logger.addHandler(handler)
