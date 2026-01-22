FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV PYTHONPATH=/app
ENV FLASK_APP=app.main:create_app
ENV FLASK_ENV=production

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
