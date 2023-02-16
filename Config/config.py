import os

class Config:
    CORS_HEADERS = 'Content-Type'
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)


class ProductionConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    
