import logging

from rq import Connection, Queue, Worker

from mote import redis

listen = ["tasks"]

if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    log = logging.getLogger("tasks")
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)

    with Connection(redis.conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
