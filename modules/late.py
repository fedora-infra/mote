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

import json
from time import ctime
import urllib.request as ulrq


seconds_delta = 86400


def fetch_recent_meetings(days):
    try:
        datagrepper_base_url = "https://apps.fedoraproject.org"
        topic = "org.fedoraproject.prod.meetbot.meeting.complete"
        source = "{}/datagrepper/raw?delta={}&topic={}".format(datagrepper_base_url, days * seconds_delta, topic)
        parse_object = json.loads(ulrq.urlopen(source).read().decode())
        meeting_rawlist = parse_object["raw_messages"]
        meeting_dict = {}
        for indx in meeting_rawlist:
            data = indx["msg"]
            logs_url = data["url"].replace("https://meetbot.fedoraproject.org", "") + ".log.html"
            summary_url = data["url"].replace("https://meetbot.fedoraproject.org", "") + ".html"
            meeting_dict[data["details"]["time_"]] = {
                "meeting_topic": data["meeting_topic"],
                "url": {
                    "logs": logs_url,
                    "summary": summary_url
                },
                "channel": data["channel"],
                "time": ctime(data["details"]["time_"])
            }
        return True, meeting_dict
    except Exception as expt:
        return False, {"exception": str(expt)}
