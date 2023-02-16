import os
import redis
from redis import Redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from Config.init import load_config

listen = ['ai-prompt']

load_dotenv()
ENV = os.getenv('ENV', 'prod')
config = load_config(ENV)

logger.info(f"Worker connecting to Redis at host={config.REDIS_HOST}, port={config.REDIS_PORT}...")
store = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
logger.info("Worker Redis connection started")

if __name__ == '__main__':
    with Connection(store):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
