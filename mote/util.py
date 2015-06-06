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
from werkzeug.routing import BaseConverter
import memcache, soke

def filter_list(li, word):
    res_list = sorted(li, key=lambda k: len(k['name']))
    return res_list

class RegexConverter(BaseConverter):
    # flask URL regex converter
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
def get_meeting_type(extension):
    if extension == "html":
        return "minutes"
    elif extension == "log.html":
        return "logs"
    else:
        # if plain-text file
        return "plain-text"
