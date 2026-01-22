FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home appuser
USER appuser

COPY app/ ./app/

EXPOSE 5000

CMD ["flask", "--app", "app:", "run", "--host=0.0.0.0"]


