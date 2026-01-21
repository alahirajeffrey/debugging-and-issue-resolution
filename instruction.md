# Flask Microservice

Instrument a sample Python Flask microservice. The microservice should emit structured logs with correlation IDs, expose Prometheus metrics, generate distributed traces via OpenTelemetry with exporters configured for local Jarger and Prometheus instances. Extend CI pipeline to lint and run tests to validate log schema conformity, metrics endpoint responses and correctness of generated trace spans

## Requirements

Requirements to run the project:

1. Docker compose

This project should:

1. Create a flask microservice
2. Setup prometheus and jaeger using docker compose
3. Expose prometheus metrics and traces via opentelemetry and jaeger
4. Pass tests to validate log schema
5. Pass tests to validate metric endpoint responses
6. Create CI pipeline to run lints and tests to ensure log schema and metric responses are correct
