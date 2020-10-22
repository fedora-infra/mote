# -*- coding: utf-8 -*-
#
# Copyright © 2015-2016 Chaoyi Zha <cydrobolt@fedoraproject.org>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import requests, json
from . import util

seconds_delta = 86400;
topic = 'org.fedoraproject.prod.meetbot.meeting.complete';

def get_latest_meetings():
    config = util.config()
    url_template = "{}/datagrepper/raw?delta={}&topic={}".format(config.datagrepper_base_url, seconds_delta, topic)

    # fetch meetings from the last day using datagrepper
    last_day_raw = requests.get(url_template)

    if not bool(last_day_raw):
        return []

    last_day = json.loads(last_day_raw.text)['raw_messages']

    # keep five latest meetings
    last_day_truncated = [k['msg'] for k in last_day[:4]]

    return last_day_truncated
