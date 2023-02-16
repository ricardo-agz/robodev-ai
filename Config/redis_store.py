import os
from dotenv import load_dotenv
from redis import Redis
import logging
from Config.init import load_config
from Config.logger import logger

load_dotenv()
ENV = os.getenv('ENV', 'prod')
config = load_config(ENV)

if config.REDISCLOUD_URL:
    logger.info(f"Connecting to Redis at {config.REDISCLOUD_URL}...")
    store = Redis.from_url(config.REDISCLOUD_URL, db=0)
else:
    logger.info(f"Connecting to Redis at host={config.REDIS_HOST}, port={config.REDIS_PORT}...")
    store = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
logger.info("Redis started")

store = store
