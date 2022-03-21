import logging
import os
import urllib.request

from mote import app, cache
from mote.modules.find import get_meetings_files


def build_cache():
    logging.info("rebuilding cache")
    cache.delete_memoized(get_meetings_files)
    get_meetings_files()


def process_new_meet(meet):
    # reformat meetboot-raw url
    # https://meetbot.fedoraproject.org/fedora-blocker-review/2022-03-21/f36-blocker-review.2022-03-21-16.01
    basepath = meet["url"].replace(app.config["MEETBOT_URL"], "")
    log_url = app.config["MEETBOT_RAW_URL"] + basepath + ".log.html"
    log_path = app.config["MEETING_DIR"] + basepath + ".log.html"
    smry_url = app.config["MEETBOT_RAW_URL"] + basepath + ".html"
    smry_path = app.config["MEETING_DIR"] + basepath + ".html"
    logging.info(f"Creating dir {os.path.dirname(smry_path)}")
    os.makedirs(os.path.dirname(smry_path), exist_ok=True)
    logging.info(f"downloading {smry_url}...")
    urllib.request.urlretrieve(smry_url, smry_path)
    logging.info(f"downloading {log_url}...")
    urllib.request.urlretrieve(log_url, log_path)
    # TODO: clear cache
