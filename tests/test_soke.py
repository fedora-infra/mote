# -*- coding: utf-8 -*-
#
# Copyright © 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
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

import sys
sys.path.insert(1, '..')

from mote import soke, util

def test_date_fn():
    dummy_filenames = [
        ("fesco.2016-01-08-17.22.html", "2016-01-08"),
        ("fesco.2015-04-01-18.00.html", "2015-04-01"),
        ("fedora-meeting-1.2014-02-04-20.11.html", "2014-02-04"),
        ("fedora-meeting-1.2013-12-09-16.34.html", "2013-12-09")
    ]

    false_filenames = [
        "not-a-date.html",
        "does-not-contain-date.2014-02.html"
    ]

    for fn in dummy_filenames:
        date = soke.get_date_fn(fn[0])
        assert date == fn[1]

    for fn in false_filenames:
        try:
            soke.get_date_fn(fn)
            raise AssertionError("Did not catch incorrect filename.")
        except ValueError:
            # expected ValueError
            continue

def test_run():
    soke.run()

    json_team_cache = util.get_json_cache("team")
    json_channel_cache = util.get_json_cache("channel")
    print json_team_cache, json_channel_cache
    channel_meeting_1 = json_channel_cache["fedora-meeting-1"]["2014-02-04"]["minutes"][0]

    team_meeting_1_minutes = json_team_cache["team_one"]["2014-02-04"]["minutes"][0]
    team_meeting_1_logs = json_team_cache["team_one"]["2014-02-04"]["logs"][0]

    assert channel_meeting_1 == "fedora-meeting-1.2014-02-04-20.11.html"

    assert team_meeting_1_minutes == "team_one.2014-02-04-20.11.html"
    assert team_meeting_1_logs == "team_one.2014-02-04-20.11.log.html"
