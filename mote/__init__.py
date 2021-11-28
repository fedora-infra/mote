"""
    Copyright (c) 2021 Fedora Websites and Apps

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import logging
import os

import rq
from flask import Flask
from flask_caching import Cache
from flask_socketio import SocketIO
from redis import Redis

__version__ = "0.7.0"


app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config.from_prefixed_env()

if app.config["CACHE_TYPE"] == "RedisCache":
    app.redis = Redis.from_url(app.config["CACHE_REDIS_URL"])
    app.task_queue = rq.Queue("tasks", connection=app.redis, default_timeout=60 * 10)
    socketio = SocketIO(app, message_queue=app.config["CACHE_REDIS_URL"])
else:
    socketio = SocketIO(app)

cache = Cache(app)
loglevel = logging.INFO
if os.environ.get("LOGLEVEL") and os.environ.get("LOGLEVEL").isnumeric():
    loglevel = int(os.environ.get("LOGLEVEL"))
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=loglevel)
