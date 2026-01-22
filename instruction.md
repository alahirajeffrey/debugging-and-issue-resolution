# Flask Microservice

Instrument a sample Python Flask microservice. The microservice should emit structured logs with correlation IDs, expose Prometheus metrics, generate distributed traces via OpenTelemetry with exporters configured for local Jarger and Prometheus instances. Extend CI pipeline to lint and run tests to validate log schema conformity, metrics endpoint responses and correctness of generated trace spans

## Requirements

Requirements to run the project:

1. Docker compose

How to run:

1. Navigate to the directory
2. Run the command `docker compose up --build` to build the application
3. Create a `.env` file and populate with the `.env.example file`
4. Then run the command `docker compose up -d`
5. Open postman and make a request to `localhost:5000/health` to run the health checker or `localhost:5000/metrics` to view the exposed prometheus metrics

This project should:

1. Create a flask microservice
2. Setup prometheus and jaeger using docker compose
3. Expose prometheus metrics and traces via opentelemetry and jaeger
4. Pass tests to validate log schema
5. Pass tests to validate metric endpoint responses
6. Create CI pipeline to run lints and tests to ensure log schema and metric responses are correct
