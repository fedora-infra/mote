# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
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

[ -n "$PYTHON" ] || PYTHON=python2

BLUE='\e[0;34m'

OFF='\e[0m'


echo -e "${BLUE} Setting up test environment..."
# copy mock configuration file

mv mote/config.py mote/config.py.bak || true

cp files/test_config.py mote/config.py

# create directory for dummy data
mkdir -p test_tmp
cd test_tmp

# create dummy meetbot data
mkdir meetbot_data

cd meetbot_data
mkdir -p fedora-meeting-1/2014-02-04
mkdir -p fedora-meeting/2014-02-04
mkdir -p teams/team_one

touch fedora-meeting-1/2014-02-04/fedora-meeting-1.2014-02-04-20.11.html
touch fedora-meeting/2014-02-04/fedora-meeting.2014-02-04-20.11.html

touch teams/team_one/team_one.2014-02-04-20.11.html
touch teams/team_one/team_one.2014-02-04-20.11.log.html

# return to test_tmp
cd ..

# return to project root
cd ..

echo -e "${BLUE} Running pyflakes...${OFF}"

"$PYTHON" -m pyflakes mote
"$PYTHON" -m pyflakes tests

echo -e "${BLUE} Running nosetests...${OFF}"

"$PYTHON" -m nose --verbose
NOSERETURN=$?

echo -e "${BLUE} Cleaning up...${OFF}"

rm -rf test_tmp
mv mote/config.py.bak mote/config.py || true

exit $NOSERETURN
