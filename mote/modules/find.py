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

import json
import os
import re
import urllib.parse as ulpr
from datetime import datetime

from mote import app, cache, logging


def get_meetings_files():
    files_list = cache.get("meetings_files")
    if files_list is None:
        files_list = []
        directory_path = f"{os.path.dirname(app.config['MEETING_DIR'])}"
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".log.html") and not root.startswith(
                    app.config["MEETING_DIR"] + "/teams/"
                ):
                    # validate path format
                    # rootpath/<channel>/<datestr>/<file.log.html>
                    full_path = os.path.join(root, file)
                    if re.search(
                        r"\/?(?P<channel>[^/]+)\/(?P<datestr>\d{4}-\d{2}-\d{2})\/(?P<filename>[^/]+\.log\.html)$",  # noqa
                        full_path,
                    ):
                        files_list.append((root, file))
                    else:
                        logging.error(f"discarding invalid meeting file: {full_path}")
        logging.info("get_meetings_files cache built")
        cache.set("meetings_files", files_list)
    return files_list


def find_meetings_by_substring(search_string: str):
    """
    Return list of meetings returned from search
    """
    try:
        meeting_dictionary = []
        allMeetFiles = get_meetings_files()
        for root, file in allMeetFiles:
            if search_string in file:
                location = f"{root}/{str(file)}"
                location_list = location.replace(app.config["MEETING_DIR"] + "/", "").split("/")
                channel_name, meeting_date, meeting_filename = (
                    location_list[0],
                    location_list[1],
                    location_list[2],
                )
                formatted_timestamp = datetime.strptime(meeting_date, "%Y-%m-%d")
                datestring = "{:%b %d, %Y}".format(formatted_timestamp)
                if ".log.html" in meeting_filename:
                    meeting_log_filename = meeting_filename
                    meeting_summary_filename = meeting_filename.replace(".log.html", ".html")
                    meeting_title = re.search(
                        app.config["RECOGNIITION_PATTERN"],
                        meeting_filename.replace(".log.html", ""),
                    )
                    meeting_object = {
                        "topic": meeting_title.group(1),
                        "channel": channel_name,
                        "date": datestring,
                        "time": meeting_title.group(3),
                        "url": {
                            "logs": f"{app.config['MEETBOT_RAW_URL']}/{channel_name}/{meeting_date}/{meeting_log_filename}",  # noqa
                            "summary": f"{app.config['MEETBOT_RAW_URL']}/{channel_name}/{meeting_date}/{meeting_summary_filename}",  # noqa
                        },
                        "slug": {
                            "logs": ulpr.quote(
                                f"/{channel_name}/{meeting_date}/{meeting_log_filename}",
                                safe=":/?",
                            ),
                            "summary": ulpr.quote(
                                f"/{channel_name}/{meeting_date}/{meeting_summary_filename}",  # noqa
                                safe=":/?",
                            ),
                        },
                    }
                    meeting_dictionary.append(meeting_object)
        return True, meeting_dictionary
    except Exception as expt:
        logging.exception(expt)
        return False, {"exception": str(expt)}


if __name__ == "__main__":
    print(json.dumps(find_meetings_by_substring(input()), indent=4))
