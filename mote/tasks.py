import logging

from mote import cache
from mote.modules.find import get_meetings_files


def build_cache():
    logging.info("rebuilding cache")
    cache.delete_memoized(get_meetings_files)
    get_meetings_files()
