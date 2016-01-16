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

import os
from os import path

'''
Mock configuration file for testing.

Crawler Configuration
'''
cwd = os.getcwd()

log_endpoint = path.abspath(path.join(cwd, 'test_tmp/meetbot_data'))

# Fedora has a "teams" folder which contains
# logs from meetings started with a certain team name
# for instance, `#startmeeting famna` will save in "/teams/famna"
# Folders not in "teams" reflect the channel name of the meeting
log_team_folder = "teams"

# Directories to ignore in crawling the logs.
# These folders are ignored. The "meetbot" folder is
# an infinite loop on Fedora's meetbot instance.
ignore_dir = "meetbot"

# Location where raw logs/minutes are stored (remote location)
meetbot_prefix = "http://meetbot-raw.fedoraproject.org"

# Location to fetch raw logs/minutes from (remote or local location)
meetbot_fetch_prefix = "http://meetbot-raw.fedoraproject.org"

# Time (in seconds) after which the log/meeting cache expires
cache_expire_time = 60 * 60 * 1


'''
Development Configuration
'''

enable_debug = True
app_port = 5000
app_host = "127.0.0.1"

'''
General Configuration
'''

# admin_groups currently has no effect on the application
# it is reserved for future use
admin_groups = ["sysadmin-mote"]
memcached_ip = "127.0.0.1:11211"
# memcached must be installed for this feature
use_memcached = False # Use a memcached store for greater performance

# JSON cache store location
json_cache_location = path.abspath(path.join(cwd, "test_tmp/cache.json"))

# Use group/name mappings fetched from GitHub
use_mappings_github = False

# If use_mappings_github is False, set alternate path
name_mappings_path = path.abspath(path.join(cwd, "name_mappings.json"))
category_mappings_path = path.abspath(path.join(cwd, "category_mappings.json"))
