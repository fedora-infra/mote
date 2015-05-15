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

# TODO: needs some regex group stuff
# get regexes and stuff from a db
import flask, peewee, random, string, pylibmc, json
from flask import Flask, render_template, request, url_for, session, redirect
from flask_fas_openid import fas_login_required, cla_plus_one_required, FAS
from database import *

mc = pylibmc.Client(["127.0.0.1"], binary=True,
                    behaviors={"tcp_nodelay": True, "ketama": True})

__version__ = "0.0.0"

user_sessions = dict()

app = Flask("mote")
fas = FAS(app)
app.secret_key = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20))
app.config['FAS_OPENID_ENDPOINT'] = 'http://id.fedoraproject.org/'
app.config['FAS_CHECK_CERT'] = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/post_auth', methods=['GET'])
@fas_login_required
def post_auth():
    session['logged'] = True
    return redirect(url_for('index'))

@app.route('/search_sugg', methods=['GET'])
def search_sugg():
    search_term = request.args.get('q', '')
    channel_meetings = mc["mote:channel_meetings"]
    team_meetings = mc["mote:team_meetings"]
    results = []
    res_num = 0
    display_num = 20
    # return top 20 search results
    # TODO: match friendly names
    for cmk in channel_meetings:
        # cmk = meeting group name
        if res_num >= display_num:
            break
        if search_term in cmk:
            results.append({"id": cmk, "name": cmk, "type": "channel", "description": "A friendly meeting group."})
            res_num += 1
    for tmk in team_meetings:
        # tmk = meeting group name
        if res_num >= display_num:
            break
        if search_term in tmk:
            results.append({"id": tmk, "name": tmk, "type": "team", "description": "A friendly meeting group."})
            res_num += 1
    results_json = json.dumps(results)
    return ('''
    {"items": %s}
    ''' % results_json)

@app.route('/auth', methods=['GET'])
def auth_login():
    groups = config.admin_groups
    next_url = url_for('post_auth')
    return fas.login(return_url=next_url, groups=groups)

@app.route('/logout', methods=['GET'])
def logout():
    if flask.g.fas_user:
        fas.logout()
        session['logged'] = None
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET'])
@fas_login_required
def admin_panel():
    is_admin = False
    for admin_group in config.admin_groups:
        if admin_group in flask.g.fas_user.groups:
            is_admin = True
    if is_admin == True:
        return render_template("admin.html")
    else:
        return render_template('error.html', error="Your account does not have access to this resource.")

@app.route('/browse', methods=['GET'])
def browse():
    channel_meetings = mc["mote:channel_meetings"]
    team_meetings = mc["mote:team_meetings"]
    return render_template('browse.html', channel_meetings=channel_meetings, team_meetings=team_meetings)
