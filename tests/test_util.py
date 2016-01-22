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

import sys, os
from os import path
sys.path.insert(1, '..')

from mote import util

cwd = os.getcwd()

def test_folder_exists():
    new_dir_path = path.join(cwd, 'test_tmp/test_create/test')
    util.check_folder_exists(new_dir_path)

    assert os.path.isdir(path.abspath(path.join(new_dir_path, '..'))) == True

def test_json_cache():
    channel_data = {
        "one": "two",
        "three": "four"
    }
    team_data = {
        "five": "six",
        "seven": "eight"
    }
    util.set_json_cache(channel_data, team_data, 10000)

    json_cache_team = util.get_json_cache("team")
    json_cache_channel = util.get_json_cache("channel")

    assert json_cache_team == team_data
    assert json_cache_channel == channel_data
