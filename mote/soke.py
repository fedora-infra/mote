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

# mote searching module
# first match teams/expressions
# then its children are made into categories within the team
# e.g date
# link files through the file extension

import pylibmc, config, os, json, re, peewee
from glob import glob
from os.path import join, getsize, split, abspath

# the `mc` variable is used to map to memcached
mc = pylibmc.Client(["127.0.0.1"], binary=True,
                    behaviors={"tcp_nodelay": True, "ketama": True})
def memcached_dict_add(dictn, key, val, cxn=mc):
    # cxn = memcached connection
    # dictn = name of remote dictionary to modify
    # key = key to add
    # val = value of key
    u_dictn = mc[dictn]
    u_dictn[key] = val
    mc[dictn] = u_dictn


# print json.dumps(["ah", "bah"])
meetbot_root_dir = config.log_endpoint
meetbot_team_dir = config.log_team_folder


def run():
    d_channel_meetings = dict() # direct channel meetings (i.e meeting channel)
    t_channel_meetings = dict() # team channel meetings (i.e meeting topics)
    neither_date = 0

    for root, dirs, files in os.walk(meetbot_root_dir):
        '''if meetbot_team_dir in dirs:
            dirs.remove(meetbot_team_dir)'''
        '''el'''
        if config.ignore_dir in dirs:
            dirs.remove(config.ignore_dir)

        fl_expr = {
            "fedora-fr": "Fedora French",
            "fedora-meeting": "Miscellaneous"
        }
        team_expr = {
            "famna": "Fedora NA Ambassadors"
        }

        folder_name = split(root)
        curr_folder_qual_name = folder_name[1]
        is_direct_child = abspath(join(root, os.pardir)) == meetbot_root_dir
        is_direct_team_child = abspath(join(root, os.pardir)) == join(meetbot_root_dir, meetbot_team_dir)
        is_team_folder = join(meetbot_root_dir, meetbot_team_dir) == root

        if re.match("[0-9]{4}\-[0-9]{2}\-[0-9]{2}", folder_name[1]):
            # If current folder name is a date
            pass
        if re.match("fedora\-meeting\-[0-9]{1,}", split(folder_name[0])[1]):
            pass
        if is_direct_child == True:
            # if direct child of meetbot_root_dir
            if curr_folder_qual_name == meetbot_team_dir:
                # is team directory
                pass
            else:
                # if new channel
                # curr_folder_qual_name is the team name
                # create a new key for the channel
                d_channel_meetings[curr_folder_qual_name] = dict()
        elif is_direct_team_child == True:
            # if new team
            # all files under this folder will directly be the meeting logs
            t_channel_meetings[curr_folder_qual_name] = dict()
        else:
            par1_path = abspath(join(root, ".."))
            par2_path = abspath(join(root, "../.."))
            parent_group_name = split(par1_path)[1]
            # is a child of a team or a channels`
            if par2_path == meetbot_root_dir:
                # is channel meeting date
                try:
                    d_channel_meetings[parent_group_name][curr_folder_qual_name] = dict()
                    minutes = glob(join(root + ".*[0-9]{2}.html"))
                    minutes = [f for f in files if re.match('.*?[0-9]{2}\.html', f)]

                    print minutes
                except Exception as e:
                    print e
