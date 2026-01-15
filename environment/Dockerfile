FROM python:3.15-slim

WORKDIR /app

## install uv
RUN pip install uv

## copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

COPY .env ./

RUN uv pip install --system --locked

COPY . .

CMD ["python", "-m", "solution.app"]
