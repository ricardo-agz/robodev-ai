import os
from dotenv import load_dotenv
from redis import Redis
from rq import Queue
from Config.init import load_config
from Config.logger import logger

load_dotenv()
ENV = os.getenv('ENV', 'prod')
config = load_config(ENV)

if config.AZURE_REDIS_HOST and config.AZURE_REDIS_PASSWORD:
    PORT = 6380
    logger.info(f"Connecting to Redis at {config.AZURE_REDIS_HOST} on port {PORT}...")
    store = Redis(
        host=config.AZURE_REDIS_HOST,
        port=PORT,
        password=config.AZURE_REDIS_PASSWORD,
        ssl=True,
        ssl_cert_reqs=None  # set to None to avoid CERTIFICATE_VERIFY_FAILED errors
    )
else:
    logger.info(f"Connecting to Redis at host={config.REDIS_HOST}, port={config.REDIS_PORT}...")
    store = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

logger.info("Redis started")


def get_redis_conn():
    return store


def get_redis_queue():
    return Queue(connection=store)

