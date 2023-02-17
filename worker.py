import os
import signal
import redis
from redis import Redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from Config.init import load_config
from Config.redis_store import store
from Config.logger import logger
from tasks import sleep

listen = ['default']


if __name__ == '__main__':
    with Connection(store):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
