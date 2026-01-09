import logging

from rq import Queue, Worker

from mote import redis

if __name__ == "__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    log = logging.getLogger("tasks")
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)

    tasks = Queue("tasks", connection=redis.conn)

    worker = Worker([tasks], connection=redis.conn)
    worker.work()
