# 

## Requirements

1. Instrument a sample Python Flas microservice
2. The microservice should emit structured logs with correlation IDs
3. Expose Prometheus metrics
4. Generate distributed traces via OpenTelemetry with exporters configured for local Jarger and Prometheus instances
5. Extend CI pipeline to lint, validate log schema conformity, metrics endpoint responses and correctness of generated trace spansa
