import os


class Config:
    SERVICE_NAME = "debugging-and-issue-resolution"
    ENV = os.getenv("ENV", "development")
    JAEGER_HOST = os.getenv("JAEGER_HOST", "localhost")
    JAEGER_PORT = int(os.getenv("JAEGER_PORT", 6831))
