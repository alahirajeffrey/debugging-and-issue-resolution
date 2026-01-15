from opentelemetry import trace
from solution.tracer import setup_tracing
from opentelemetry.sdk.trace.export import BatchSpanProcessor


## SHOULD PASS: test to see if tracer is configured
def test_tracer_is_configured():
    tracer = trace.get_tracer(__name__)
    assert tracer is not None


## SHOULD FAIL: test to see if tracer is not configured
def test_tracer_provider_is_none():
    provider = trace.get_tracer_provider()
    assert provider is None


## SHOULD PASS: test to see if tracer is an instance of trace provier
def test_tracer_provider_is_set(client):
    setup_tracing(client.application)

    ## get the global tracer provider
    provider = trace.get_tracer_provider()
    assert provider is not None
    from opentelemetry.sdk.trace import TracerProvider

    assert isinstance(provider, TracerProvider)
