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

import os
import re
import urllib.parse as ulpr
from datetime import datetime

import bs4 as btsp
from flask import current_app as app
from markdown import markdown

from mote import logging

from . import sanitize_name


def fetch_channel_dict():
    try:
        channel_dict = {}
        chanlist = os.listdir(app.config["MEETING_DIR"])
        for channel in chanlist:
            channel_dict[channel] = f"{app.config['MEETBOT_RAW_URL']}/{channel}"
        return True, channel_dict
    except Exception as expt:
        logging.exception(expt)
        return False, {"exception": str(expt)}


def fetch_datetxt_dict(channel: str):
    try:
        datetxt_dict = {}
        datelist = os.listdir(f"{app.config['MEETING_DIR']}/{channel}")
        for datetxt in datelist:
            datetxt_dict[datetxt] = f"{app.config['MEETBOT_RAW_URL']}/{channel}/{datetxt}"
        return True, datetxt_dict
    except Exception as expt:
        logging.exception(expt)
        return False, {"exception": str(expt)}


def fetch_meeting_dict(channel: str, datetxt: str):
    try:
        meeting_list = []
        meetlist = os.listdir(f"{app.config['MEETING_DIR']}/{channel}/{datetxt}")
        formatted_timestamp = datetime.strptime(datetxt, "%Y-%m-%d")
        datestring = f"{formatted_timestamp:%b %d, %Y}"
        for meeting in meetlist:
            if ".log.html" in meeting:
                meeting_log = (
                    f"{app.config['MEETBOT_RAW_URL']}/{channel}/{datetxt}/{meeting}"  # noqa
                )
                meeting_sum = f"{app.config['MEETBOT_RAW_URL']}/{channel}/{datetxt}/{meeting.replace('''.log.html''', '''.html''')}"  # noqa
                meeting_title = re.search(
                    app.config["RECOGNIITION_PATTERN"],
                    meeting.replace(".log.html", ""),
                )
                meeting_object = {
                    "topic": sanitize_name(meeting_title.group(1)),
                    "channel": channel,
                    "date": datestring,
                    "time": meeting_title.group(3),
                    "url": {
                        "logs": meeting_log,
                        "summary": meeting_sum,
                    },
                    "slug": {
                        "logs": ulpr.quote(
                            meeting_log.replace(app.config["MEETBOT_RAW_URL"], ""),
                            safe=":/?",
                        ),
                        "summary": ulpr.quote(
                            meeting_sum.replace(app.config["MEETBOT_RAW_URL"], ""),
                            safe=":/?",
                        ),
                    },
                }
                meeting_list.append(meeting_object)
        return True, meeting_list
    except Exception as expt:
        logging.exception(expt)
        return False, {"exception": str(expt)}


def fetch_meeting_content(contpath: str):
    try:
        with open(contpath) as meetfile:
            source = meetfile.read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        contdata = parse_object.find("body").decode()
        return True, contdata
    except Exception as expt:
        logging.exception(expt)
        return False, {"exception": str(expt)}


def fetch_meeting_summary(contpath: str):
    try:
        with open(contpath) as meetfile:
            source = meetfile.read()
        obj = btsp.BeautifulSoup(source, "html.parser")
        event = {"peoples": [], "topics": [], "actions": []}
        event["title"] = re.sub(r"^.*: ", "", sanitize_name(obj.select_one("title").text))

        re_start = re.compile(r"Meeting started.* at (\d+:\d+:\d+) UTC")
        re_end = re.compile(r"Meeting ended.* at (\d+:\d+:\d+) UTC")
        timeStartStr = re.search(re_start, obj.find(string=re_start).text).group(1)
        timeEndStr = re.search(re_end, obj.find(string=re_end).text).group(1)
        timeDelta = datetime.strptime(timeEndStr, "%H:%M:%S") - datetime.strptime(
            timeStartStr, "%H:%M:%S"
        )
        event["duration"] = timeDelta.seconds // 60

        peoples = obj.find(string=re.compile("People present")).parent.findNext("ol").select("li")
        # filter known bots and people with 0 lines
        event["peoples"] = [
            p.text for p in peoples if re.match(r"^(?!(zodbot|fm-admin))((?!\(0\)).)*$", p.text)
        ]

        topics = obj.select(".TOPIC")
        topics = (
            obj.find("h3", string="Meeting summary")
            .parent.findNext("ol")
            .findChildren("li", recursive=False)
        )
        for topic in topics:
            topicName = "None"
            topicEl = topic.findNext("b", {"class": "TOPIC"})
            if topicEl:
                topicName = topicEl.text
            topicDict = {"title": topicName, "info": []}
            items = topic.select("li")
            for item in items:
                item.findNext("span", {"class": "details"}).decompose()
                topicDict["info"].append(re.sub(r"\s+", " ", item.text))
            event["topics"].append(topicDict)
        actions = obj.find(string="Action items").parent.findNext("ol").select("li")
        event["actions"] = [a.text for a in actions if a.text != "(none)"]

        summary_path = contpath.replace(".html", ".summary.md")
        event["summary"] = None
        if os.path.exists(summary_path):
            with open(summary_path) as fh:
                event["summary"] = markdown(fh.read())

        return True, event
    except Exception as expt:
        logging.exception(expt)
        return False, {"exception": str(expt)}
