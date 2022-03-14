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

import glob
import json
import os
import os.path
import re
import urllib.request as ulrq
from datetime import datetime, timedelta

from mote import app, cache

from . import sanitize_name
from .call import fetch_meeting_summary

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


@cache.memoize(timeout=3600)
def fetch_meeting_by_day(dateStr):
    meets = []
    meet_path = app.config["MEETING_DIR"]
    meetlogs = glob.glob(f"{meet_path}/*/{dateStr}/*.log.html")
    if len(meetlogs):
        for meetfile in meetlogs:
            meet = fetch_meeting_summary(meetfile.replace(".log.html", ".html"))
            meeting = re.search(
                app.config["RECOGNIITION_PATTERN"],
                os.path.basename(meetfile.replace(".log.html", "")),
            )
            date = datetime.strptime(f"{meeting.group(2)} {meeting.group(3)}", "%Y-%m-%d %H.%M")
            meets.append(
                {
                    "title": meet[1]["title"],
                    "start": date.isoformat(),
                    "allDay": False,
                    "display": "block",
                    "attendees": len(meet[1]["peoples"]),
                    "topics": len(meet[1]["topics"]),
                    "length": meet[1]["duration"],
                    "url": meetfile.replace(app.config["MEETING_DIR"], "").replace(".log", ""),
                }
            )
    return meets


def fetch_meeting_by_period(start, end):
    meets = []
    start_date = datetime.fromisoformat(start)
    end_date = datetime.fromisoformat(end)
    cur_date = start_date
    while cur_date <= end_date:
        meets += fetch_meeting_by_day(cur_date.strftime("%Y-%m-%d"))
        cur_date += timedelta(days=1)
    return meets


def fetch_meetings_from_datagreeper(start):
    """For testing purpose only
    to be removed before release"""
    try:
        topic = "org.fedoraproject.prod.meetbot.meeting.complete"
        source = "{}/datagrepper/raw?start={}&topic={}".format(
            app.config["DATAGREPPER_BASE_URL"], start.isoformat(), topic
        )
        print(source)
        parse_object = json.loads(ulrq.urlopen(source).read().decode())
        meeting_rawlist = parse_object["raw_messages"]
        meeting_list = []
        total_pages = parse_object["pages"]
        cur_page = 1
        while cur_page <= total_pages:
            for indx in meeting_rawlist:
                data = indx["msg"]
                meeting = re.search(
                    app.config["RECOGNIITION_PATTERN"],
                    data["url"].replace(app.config["MEETBOT_URL"], "").replace(".log.html", ""),
                )
                date = datetime.strptime(f"{meeting.group(2)} {meeting.group(3)}", "%Y-%m-%d %H.%M")
                meeting_list.append(
                    {
                        "title": sanitize_name(data["meeting_topic"]),
                        "start": date.isoformat(),
                        "allDay": False,
                        "display": "block",
                        "url": data["url"] + ".html",
                        "attendees": len(data["attendees"]),
                        "lines": data["details"]["linenum"],
                    }
                )
            cur_page += 1
            if cur_page <= total_pages:
                source = "{}/datagrepper/raw?start={}&topic={}&page={}".format(
                    app.config["DATAGREPPER_BASE_URL"],
                    start.isoformat(),
                    topic,
                    cur_page,
                )
                print(source)
                parse_object = json.loads(ulrq.urlopen(source).read().decode())
                meeting_rawlist = parse_object["raw_messages"]

        return meeting_list
    except Exception:
        raise
        return []
