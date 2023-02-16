import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CORS_HEADERS = 'Content-Type'
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDISCLOUD_URL = os.getenv("REDISCLOUD_URL")
    FLASK_PORT = os.getenv("FLASK_PORT", 8000)


class ProductionConfig(Config):
    DEBUG = False
    ENV = "prod"


class DevConfig(Config):
    DEBUG = True
    ENV = "dev"
    
