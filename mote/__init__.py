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

import flask, peewee, random, string, pylibmc, json, util
import dateutil.parser, operator
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

def return_error(msg):
    return render_template('error.html', error=msg)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/post_auth', methods=['GET'])
@fas_login_required
def post_auth():
    session['logged'] = True
    return redirect(url_for('index'))

@app.route('/request_logs', methods=['GET', 'POST'])
def request_logs():
    if request.method == "GET":
        return return_error("400 Bad Request")
    else:
        group_id = request.form["group_id"]
        group_type = request.form["group_type"]
        # Meeting date
        date_stamp = request.form["date_stamp"]
        if group_type == "team":
            meetings = mc["mote:team_meetings"]
        elif group_type == "channel":
            meetings = mc["mote:channel_meetings"]
        try:
            workable_array = meetings[group_id][date_stamp]
            # lists with links to minutes and logs
            minutes = workable_array["minutes"]
            logs = workable_array["logs"]

            response = json.dumps({"minutes": minutes, "logs": logs})
            return response
        except:
            return return_error("404 Not Found")

@app.route('/sresults', methods=['GET'])
def sresults():
    group_id = request.args.get('group_id', '')
    group_type = request.args.get('type', '')
    friendly_name = False
    if (group_id == '') or (group_type == ''):
        return return_error("Invalid group ID or type.")

    if group_type == "team":
        meetings = mc["mote:team_meetings"]
    elif group_type == "channel":
        meetings = mc["mote:channel_meetings"]
    else:
        return return_error("Invalid group type.")
    try:
        # set meetings to specific group meetings only
        groupx_meetings = meetings[group_id]
    except:
        return return_error("Group not found.")
    try:
        avail_dates = dict()
        # avail_dates[year][month][year-month-day]
        for date in groupx_meetings:
            parsed_date = dateutil.parser.parse(date)
            month = parsed_date.strftime("%B")
            year = parsed_date.year
            if year not in avail_dates:
                avail_dates[year] = dict()
            if month not in avail_dates[year]:
                avail_dates[year][month] = []
            avail_dates[year][month].append(date)
        # structure: groupx_meetings[meeting_date]["minutes"]
    except:
        pass

    return render_template('sresults.html',
        friendly_name = friendly_name,
        name = group_id,
        type = group_type,
        avail_dates = avail_dates
    )
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
    results = util.filter_list(results, search_term) # sort results
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
