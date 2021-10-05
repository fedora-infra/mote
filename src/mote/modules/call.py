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

import bs4 as btsp

from config import BASE_URL

recognition_pattern = "(.*)[\-\.]([0-9]{4}-[0-9]{2}-[0-9]{2})-([0-9]{2}\.[0-9]{2})"


def fetch_channel_dict():
    try:
        channel_dict = {}
        chanlist = os.listdir("/srv/web/meetbot")
        for channel in chanlist:
            channel_dict[channel] = BASE_URL + "/%s" % channel
        return True, channel_dict
    except Exception as expt:
        return False, {"exception": str(expt)}


def fetch_datetxt_dict(channel: str):
    try:
        datetxt_dict = {}
        datelist = os.listdir("/srv/web/meetbot/%s" % channel)
        for datetxt in datelist:
            datetxt_dict[datetxt] = BASE_URL + "/%s/%s" % (
                channel,
                datetxt,
            )
        return True, datetxt_dict
    except Exception as expt:
        return False, {"exception": str(expt)}


def fetch_meeting_dict(channel: str, datetxt: str):
    try:
        meeting_list = []
        meetlist = os.listdir("/srv/web/meetbot/%s/%s" % (channel, datetxt))
        for meeting in meetlist:
            if ".log.html" in meeting:
                meeting_log = BASE_URL + "/%s/%s/%s" % (
                    channel,
                    datetxt,
                    meeting,
                )
                meeting_sum = BASE_URL + "/%s/%s/%s" % (
                    channel,
                    datetxt,
                    meeting.replace(".log.html", ".html"),
                )
                meeting_title = re.search(
                    recognition_pattern,
                    meeting.replace(".log.html", ""),
                )
                meeting_object = {
                    "topic": meeting_title.group(1),
                    "channel": channel,
                    "date": datetxt,
                    "time": meeting_title.group(3),
                    "url": {
                        "logs": meeting_log,
                        "summary": meeting_sum,
                    },
                    "slug": {
                        "logs": ulpr.quote(
                            meeting_log.replace(
                                BASE_URL, ""
                            ),
                            safe=":/?",
                        ),
                        "summary": ulpr.quote(
                            meeting_sum.replace(
                                BASE_URL, ""
                            ),
                            safe=":/?",
                        ),
                    },
                }
                meeting_list.append(meeting_object)
        return True, meeting_list
    except Exception as expt:
        return False, {"exception": str(expt)}


def fetch_meeting_content(contpath: str):
    try:
        with open(contpath, "r") as meetfile:
            source = meetfile.read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        contdata = parse_object.find("body").decode()
        return True, contdata
    except Exception as expt:
        return False, ""
