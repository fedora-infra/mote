import logging
import os

from flask_socketio import SocketIO

from mote import app, cache
from mote.modules.find import get_meetings_files
from mote.modules.late import fetch_meeting_by_day, get_meeting_info

REDIS_URL = os.environ.get("REDIS_URL") or "redis://"
socketio = SocketIO(message_queue=REDIS_URL)


def build_cache():
    logging.info("rebuilding cache")
    cache.delete("meetings_files")
    get_meetings_files()


def process_new_meet(meet):
    # reformat meetboot-raw url
    # https://meetbot.fedoraproject.org/fedora-blocker-review/2022-03-21/f36-blocker-review.2022-03-21-16.01
    basepath = meet["url"].replace(app.config["MEETBOT_URL"], "")

    meetlog_path = app.config["MEETING_DIR"] + basepath + ".log.html"

    # clear cache
    cache.delete_memoized(fetch_meeting_by_day, basepath.split("/")[2])

    # add files to file_cache (root, file)
    file_cache = cache.get("meetings_files")
    file_cache.append((os.path.dirname(meetlog_path), os.path.basename(meetlog_path)))
    cache.set("meetings_files", file_cache)

    # send new event to clients
    event = get_meeting_info(app.config["MEETING_DIR"] + basepath)
    socketio.emit("add_event", event)
