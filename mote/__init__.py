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

import collections

import flask, peewee, random, string, pylibmc, json, util, os
import dateutil.parser, requests, collections
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for, session, redirect
from flask_fas_openid import fas_login_required, cla_plus_one_required, FAS

mc = pylibmc.Client([config.memcached_ip], binary=True,
                    behaviors={"tcp_nodelay": True, "ketama": True})

__version__ = "0.0.0"

user_sessions = dict()

app = Flask("mote")
fas = FAS(app)
app.secret_key = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20))
app.config['FAS_OPENID_ENDPOINT'] = 'http://id.fedoraproject.org/'
app.config['FAS_CHECK_CERT'] = True
cwd = os.getcwd()
with open(os.path.join(cwd, 'name_mappings.json')) as data_file:
    name_mappings = json.load(data_file)

with open(os.path.join(cwd, 'category_mappings.json')) as data_file:
    category_mappings = json.load(data_file)

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

@app.route('/get_meeting_log', methods=["GET", "POST"])
def get_meeting_log():
    if request.method == "GET":
        return return_error("400 Bad Request")
    else:
        group_type = request.form['group_type']
        date_stamp = request.form['date_stamp']
        group_id = request.form['group_id']
        file_name = request.form['file_name']

        if group_type == "team":
            link_prefix = config.meetbot_prefix+"/teams/" + group_id + "/"
        else:
            link_prefix = config.meetbot_prefix+ "/" + group_id + "/" + date_stamp + "/"
        url = link_prefix + file_name
        try:
            fetch_result = requests.get(url)
            fetch_soup = BeautifulSoup(fetch_result.text)
            body_content = str(fetch_soup.body)
            body_content = body_content.replace("</br>", "")
            return body_content
        except Exception as e:
            return "404"

@app.route('/sresults', methods=['GET'])
def sresults():
    group_id = request.args.get('group_id', '')
    group_type = request.args.get('type', '')
    try:
        friendly_name = name_mappings[group_id]["friendly-name"]
    except:
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

    sorted_dates = list(groupx_meetings.keys())
    sorted_dates.sort(key=dateutil.parser.parse)

    avail_dates = collections.OrderedDict()
    # avail_dates[year][month][year-month-day]

    try:
        for date in sorted_dates:
            parsed_date = dateutil.parser.parse(date)
            month = parsed_date.strftime("%B")
            year = parsed_date.year
            if year not in avail_dates:
                avail_dates[year] = collections.OrderedDict()
            if month not in avail_dates[year]:
                avail_dates[year][month] = []
            avail_dates[year][month].append(date)
        sorted_date_items = avail_dates.items()
        sorted_date_items.reverse()
        avail_dates = collections.OrderedDict(sorted_date_items)
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
    for cmk in channel_meetings:
        # cmk = meeting group name
        if res_num >= display_num:
            # if 20 results are already found
            break
        if search_term in cmk:
            # if the term corresponds, match its friendly name and add its name
            # to the list of results
            try:
                friendly_name = name_mappings[cmk]["friendly-name"]
            except:
                friendly_name = "A friendly meeting group."

            results.append({"id": cmk, "name": cmk, "type": "channel", "description": friendly_name})
            res_num += 1
    for tmk in team_meetings:
        # tmk = meeting group name
        if res_num >= display_num:
            # if 20 results already found
            break
        if search_term in tmk:
            try:
                friendly_name = name_mappings[tmk]["friendly-name"]
            except:
                friendly_name = "A friendly meeting group."

            results.append({"id": tmk, "name": tmk, "type": "team", "description": friendly_name})
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
    browse_nmappings = dict()
    for category_index in category_mappings:
        for category in category_mappings[category_index]:
            try:
                browse_nmappings[category] = name_mappings[category]["friendly-name"]
            except:
                browse_nmappings[category] = category
    return render_template('browse.html', category_mappings=category_mappings, browse_nmappings=browse_nmappings)
