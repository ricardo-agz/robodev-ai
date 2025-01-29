from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from generator.Config.redis_store import store

listen = ['default']


if __name__ == '__main__':
    with Connection(store):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
