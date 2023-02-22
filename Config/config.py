import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CORS_HEADERS = 'Content-Type'
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDISCLOUD_URL = os.getenv("REDISCLOUD_URL")
    AZURE_REDIS_HOST = os.getenv("AZURE_REDIS_HOST")
    AZURE_REDIS_PASSWORD = os.getenv("AZURE_REDIS_PASSWORD")
    FLASK_PORT = os.getenv("FLASK_PORT", 8000)


class ProductionConfig(Config):
    DEBUG = False
    ENV = "prod"
    NEUTRINO_IDENTITY_URL = os.getenv("NEUTRINO_IDENTITY_URL")


class DevConfig(Config):
    DEBUG = True
    ENV = "dev"
    NEUTRINO_IDENTITY_URL = "http://host.docker.internal:8080"
    
