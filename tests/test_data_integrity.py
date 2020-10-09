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

import sys, json
sys.path.insert(1, '..')

with open("name_mappings.json", 'r') as f:
    name_mappings = json.loads(f.read())

def test_name_mappings_integrity():
    ga = dict()

    for key, nm in name_mappings.items():
        ga[key] = True

        try:
            nm_aliases = nm["aliases"]
        except KeyError:
            continue

        for al in nm_aliases:
            if al == key:
                raise Exception("Do not include group itself as an alias in {}".format(al))
            if al in ga:
                raise ValueError("Duplicate alias in name mappings: {}".format(al))

            ga[al] = True
