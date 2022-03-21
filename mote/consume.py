import logging
import os

from fedora_messaging.api import consume
from fedora_messaging.config import conf
from flask_socketio import SocketIO

conf.setup_logging()
REDIS_URL = os.environ.get("REDIS_URL") or "redis://"
socketio = SocketIO(message_queue=REDIS_URL)


def consume_fedora_messaging_msg(message):
    logging.info(message)
    # Send client notification
    socketio.emit("show_toast", message.body)


if __name__ == "__main__":
    conf.setup_logging()
    consume(consume_fedora_messaging_msg)
