# -*- coding: utf-8 -*-
#
# Copyright © 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
#                  Ralph Bean <rbean@redhat.com>
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
import time

import fedmsg

import soke

target = '.meetbot.meeting.complete'

def main():
    for _, _, topic, msg in fedmsg.tail_messages():
        if not topic.endswith(target):
            continue

        print("A meeting just ended!  Let's sleep for 2s to dodge a race.")
        time.sleep(2)
        print("Running soke.run()...")
        soke.run()
        print("Done.")
