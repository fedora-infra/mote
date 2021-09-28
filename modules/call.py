"""
##########################################################################
*
*   Copyright © 2019-2021 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

import os
import re
import urllib.parse as ulpr

import bs4 as btsp

recognition_pattern = "(.*)[\-\.]([0-9]{4}-[0-9]{2}-[0-9]{2})-([0-9]{2}\.[0-9]{2})"


def fetch_channel_dict():
    try:
        channel_dict = {}
        chanlist = os.listdir("/srv/web/meetbot")
        for channel in chanlist:
            channel_dict[channel] = "https://meetbot-raw.fedoraproject.org/%s" % channel
        return True, channel_dict
    except Exception as expt:
        return False, {"exception": str(expt)}


def fetch_datetxt_dict(channel: str):
    try:
        datetxt_dict = {}
        datelist = os.listdir("/srv/web/meetbot/%s" % channel)
        for datetxt in datelist:
            datetxt_dict[datetxt] = "https://meetbot-raw.fedoraproject.org/%s/%s" % (
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
                meeting_log = "https://meetbot-raw.fedoraproject.org/%s/%s/%s" % (
                    channel,
                    datetxt,
                    meeting,
                )
                meeting_sum = "https://meetbot-raw.fedoraproject.org/%s/%s/%s" % (
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
                                "https://meetbot-raw.fedoraproject.org", ""
                            ),
                            safe=":/?",
                        ),
                        "summary": ulpr.quote(
                            meeting_sum.replace(
                                "https://meetbot-raw.fedoraproject.org", ""
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
