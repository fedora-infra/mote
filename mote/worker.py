import logging
import os

import redis
from rq import Connection, Queue, Worker

listen = ["tasks"]

REDIS_URL = os.environ.get("REDIS_URL") or "redis://"

conn = redis.from_url(REDIS_URL)

if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    log = logging.getLogger("tasks")
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
