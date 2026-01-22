FROM python:3.11-slim

WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

# copy requirements.txt and install
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# create non-root user
RUN useradd --create-home appuser
USER appuser

# copy app code
COPY app/ ./app/

# expose port
EXPOSE 5000

# start app
CMD ["flask", "run"]
