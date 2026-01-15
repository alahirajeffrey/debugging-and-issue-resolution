from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from solution.config import Config


def setup_tracing(app):
    resource = Resource.create(
        {"service.name": Config.SERVICE_NAME}
    )

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces"
    )

    provider.add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )

    FlaskInstrumentor().instrument_app(app)
