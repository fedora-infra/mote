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
import urllib.request as ulrq
from datetime import datetime

from flask import current_app as app

seconds_delta = 86400


def fetch_recent_meetings(days):
    try:
        topic = "org.fedoraproject.prod.meetbot.meeting.complete"
        source = "{}/datagrepper/raw?delta={}&topic={}".format(
            app.config["DATAGREPPER_BASE_URL"], days * seconds_delta, topic
        )
        parse_object = json.loads(ulrq.urlopen(source).read().decode())
        meeting_rawlist = parse_object["raw_messages"]
        meeting_dict = {}
        for indx in meeting_rawlist:
            data = indx["msg"]
            formatted_timestamp = data["details"]["time_"]
            datestring = datetime.fromtimestamp(formatted_timestamp).strftime("%b %d, %Y %I:%M:%S")
            logs_url = data["url"].replace(app.config["MEETBOT_URL"], "") + ".log.html"
            summary_url = data["url"].replace(app.config["MEETBOT_URL"], "") + ".html"
            meeting_dict[data["details"]["time_"]] = {
                "topic": data["meeting_topic"],
                "channel": data["channel"],
                "time": datestring,
                "slug": {"logs": logs_url, "summary": summary_url},
            }
        return True, meeting_dict
    except Exception as expt:
        return False, {"exception": str(expt)}
