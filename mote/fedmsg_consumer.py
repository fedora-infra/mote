# -*- coding: utf-8 -*-
#
# Copyright © 2015-2016 Chaoyi Zha <cydrobolt@fedoraproject.org>
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

from __future__ import print_function
from logging.config import dictConfig
import logging
import subprocess as sp
import time

import fedmsg
import fedmsg.config

import soke

log = logging.getLogger('fedmsg')

target = '.meetbot.meeting.complete'

def main():
    fedmsg_config = fedmsg.config.load_config()
    dictConfig(fedmsg_config.get('logging', {'version': 1}))

    log.info("Listening to the bus via fedmsg.tail_messages()")
    for _, _, topic, msg in fedmsg.tail_messages():

        # XXX - if you want to debug whether or not this is receiving fedmsg
        # messages, you can put a print statement here, before the 'continue'
        # statement.

        if not topic.endswith(target):
            continue

        log.info("A meeting just ended!  Sleeping 2s.  %r" % msg.get('msg_id'))
        time.sleep(2)

        teams_cmd = "/usr/local/bin/meetings_by_team.sh"
        log.info("Running %r" % teams_cmd)
        proc = sp.Popen(teams_cmd.split(), stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode:
            # Calling log.error in fedora infrastructure with fedmsg logging
            # configured, should send an email to the sysadmin-datanommer
            # group.
            log.error("Error %r running %r.\n  STDOUT:  %s\n  STDERR:  %s" % (
                proc.returncode, teams_cmd, stdout, stderr))

        log.info("Running soke.run()...")
        soke.run()

        log.info("Done.")
