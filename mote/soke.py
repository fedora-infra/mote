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

import memcache, os, re, sys, util
from os.path import join, split, abspath

from latest_meetings import get_latest_meetings

try:
    # if different config directory provided
    # e.g ran in mod_wsgi
    import site
    config_path = os.environ['MOTE_CONFIG_FOLDER']
    site.addsitedir(config_path) # default: "/etc/mote"
except:
    # different config directory not specified
    # e.g running from git clone
    pass

import config
reload(sys)
sys.setdefaultencoding("utf-8")

# The "mc" variable can be used to map to memcached.
if config.use_memcached == True:
    mc = memcache.Client([config.memcached_ip], debug=0)

def get_date_fn(filename):
    # Return a meeting's date from a filename.
    m = re.search(".*[\-\.]([0-9]{4}\-[0-9]{2}\-[0-9]{2}).*?\.(html|log\.html|txt|log\.txt)", filename)
    if m == None:
        raise ValueError("Failed to parse date from %r" % filename)
    return m.group(1)


meetbot_root_dir = config.log_endpoint
meetbot_team_dir = config.log_team_folder


def run():
    d_channel_meetings = dict() # channel meetings (i.e meeting channel)
    t_channel_meetings = dict() # team meetings (i.e meeting names)
    for root, dirs, files in os.walk(meetbot_root_dir):
        if config.ignore_dir in dirs:
            dirs.remove(config.ignore_dir)

        folder_name = split(root)
        curr_folder_qual_name = folder_name[1]
        is_direct_child = abspath(join(root, os.pardir)) == meetbot_root_dir
        is_direct_team_child = abspath(join(root, os.pardir)) == join(meetbot_root_dir, meetbot_team_dir)
        is_team_folder = join(meetbot_root_dir, meetbot_team_dir) == root

        if is_direct_child == True:
            # If current folder is a direct child of meetbot_root_dir.
            if curr_folder_qual_name == meetbot_team_dir:
                pass
            else:
                # If a new channel has been located.
                d_channel_meetings[curr_folder_qual_name] = dict()
        elif is_direct_team_child == True:
            # If a new team has been located.
            # All files in this folder should be the meeting logs.
            minutes = [f for f in files if re.match('.*?[0-9]{2}\.html', f)]
            logs = [f for f in files if re.match('.*?[0-9]{2}\.log\.html', f)]
            t_channel_meetings[curr_folder_qual_name] = dict()
            for minute in minutes:
                meeting_date = get_date_fn(minute)
                if meeting_date not in t_channel_meetings[curr_folder_qual_name]:
                    t_channel_meetings[curr_folder_qual_name][meeting_date] = dict()
                    t_channel_meetings[curr_folder_qual_name][meeting_date]["minutes"] = []
                    t_channel_meetings[curr_folder_qual_name][meeting_date]["logs"] = []

                t_channel_meetings[curr_folder_qual_name][meeting_date]["minutes"].append(minute)

            for log in logs:
                meeting_date = get_date_fn(log)
                t_channel_meetings[curr_folder_qual_name][meeting_date]["logs"].append(log)


        else:
            par1_path = abspath(join(root, ".."))
            par2_path = abspath(join(root, "../.."))
            parent_group_name = split(par1_path)[1]
            # is a child of a team or a channels`
            if par2_path == meetbot_root_dir:
                # If the current folder is a channel meeting folder.
                # The date represented by `curr_folder_qual_name`.
                try:
                    d_channel_meetings[parent_group_name][curr_folder_qual_name] = dict()
                    minutes = [f for f in files if re.match('.*?[0-9]{2}\.html', f)]
                    logs = [f for f in files if re.match('.*?[0-9]{2}\.log\.html', f)]
                    d_channel_meetings[parent_group_name][curr_folder_qual_name]["minutes"] = minutes
                    d_channel_meetings[parent_group_name][curr_folder_qual_name]["logs"] = logs
                except:
                    pass

    # fetch latest meetings using datagrepper for the past 24 hours
    latest_meetings = get_latest_meetings()

    if config.use_memcached == True:
        mc.set("mote:channel_meetings", d_channel_meetings, config.cache_expire_time)
        mc.set("mote:team_meetings", t_channel_meetings, config.cache_expire_time)
        mc.set("mote:latest_meetings", latest_meetings, config.cache_expire_time)

        util.set_json_cache(d_channel_meetings, t_channel_meetings, latest_meetings, config.cache_expire_time)
    else:
        util.set_json_cache(d_channel_meetings, t_channel_meetings, latest_meetings, config.cache_expire_time)
