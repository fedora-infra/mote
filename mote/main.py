"""
    Copyright (c) 2021 Fedora Websites and Apps

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import re
import urllib.parse
from datetime import datetime

import click
from flask import abort, jsonify, redirect, render_template, request, url_for

from mote import app as main
from mote import logging, socketio
from mote.__init__ import __version__
from mote.modules import sanitize_name
from mote.modules.call import (
    fetch_channel_dict,
    fetch_datetxt_dict,
    fetch_meeting_content,
    fetch_meeting_dict,
    fetch_meeting_summary,
)
from mote.modules.find import find_meetings_by_substring, get_meeting_adj
from mote.modules.late import fetch_meeting_by_period

thread = None
client_count = 0

if main.config["CACHE_TYPE"] == "RedisCache":
    rq_job = main.task_queue.enqueue("mote.tasks.build_cache")


@main.get("/fragedpt/")
def fragedpt():
    rqstdata = request.args.get("rqstdata")
    response = {}
    if rqstdata == "listchan":
        chanobjc = fetch_channel_dict()
        if chanobjc[0]:
            response = chanobjc[1]
        else:
            logging.error("Channel list could not be retrieved")

    elif rqstdata == "listdate":
        channame = request.args.get("channame")
        dateobjc = fetch_datetxt_dict(channame)
        if dateobjc[0]:
            response = dateobjc[1]
        else:
            logging.error("Date list could not be retrieved")

    elif rqstdata == "listmeet":
        channame = request.args.get("channame")
        datename = request.args.get("datename")
        meetobjc = fetch_meeting_dict(channame, datename)
        if meetobjc[0]:
            response = meetobjc[1]
        else:
            logging.error("Meeting list could not be retrieved")

    elif rqstdata == "srchmeet":
        response = []
        srchtext = request.args.get("srchtext")
        srchrslt = find_meetings_by_substring(srchtext)
        if srchrslt[0]:
            response = srchrslt[1]
        else:
            logging.error("Meetings could not be looked up:")

    return jsonify(response)


@main.get("/cal/events")
def getevents():
    start = request.args.get("start")
    end = request.args.get("end")
    return jsonify(fetch_meeting_by_period(start, end))


@main.get("/<string:channame>/<date:cldrdate>/<string:meetname>.<any('html','log.html','txt'):ext>")
def statfile(channame, cldrdate, meetname, ext):
    if ext == "log.html":
        typecont = "Logs"
    elif ext == "html":
        typecont = "Minutes"
    elif ext == "txt":
        # if txt log, redirect to meetbot-raw
        encoded_uri = urllib.parse.quote(request.path)
        return redirect(f"{main.config['MEETBOT_RAW_URL']}/{encoded_uri}", code=302)
    else:
        abort(404)

    meetpath = main.config["MEETING_DIR"] + request.path
    meetcont = fetch_meeting_content(meetpath)
    if not meetcont[0]:
        abort(404)
    else:
        meeting_title = re.search(main.config["RECOGNIITION_PATTERN"], meetname)

        return render_template(
            "statfile.html.j2",
            channame=channame,
            cldrdate=cldrdate,
            meetname=meeting_title.group(1),
            timetext=meeting_title.group(3),
            typecont=typecont,
            meetcont=meetcont[1],
        )


@main.get("/smry/<string:channame>/<date:cldrdate>/<string:meetname>.html")
def evtsmry(channame, cldrdate, meetname):
    logging.info(
        "evtsmry: channame %s, cldrdate: %s, meetname %s"
        % (
            channame,
            cldrdate,
            meetname,
        )
    )
    logging.info("evtsmry: meetname %s" % (meetname,))
    meetpath = f"{main.config['MEETING_DIR']}/{channame}/{cldrdate:%Y-%m-%d}/{meetname}.html"
    logging.info("evtsmry: meetpath %s" % (meetpath,))
    meet = fetch_meeting_summary(meetpath)
    if not meet[0]:
        abort(404)
    else:
        permalink = url_for(
            "statfile", channame=channame, cldrdate=cldrdate, meetname=meetname, ext="html"
        )
        full_log = url_for(
            "statfile", channame=channame, cldrdate=cldrdate, meetname=meetname, ext="log.html"
        )

        meeting_name_match = re.search(main.config["RECOGNIITION_PATTERN"], meetname)
        latest = url_for("get_latest_meeting", meetname=meeting_name_match.group(1))
        meeting_datetime = datetime.combine(
            cldrdate, datetime.strptime(meeting_name_match.group(3), "%H.%M").time()
        )
        _, adj_meetings = get_meeting_adj(
            sanitize_name(meeting_name_match.group(1)), meeting_datetime
        )

        return render_template(
            "event_summary.html.j2",
            meet=meet[1],
            startdate=cldrdate,
            permalink=permalink,
            latest_link=latest,
            full_log=full_log,
            adj_meetings=adj_meetings,
        )


@main.get("/latest/<string:meetname>")
def get_latest_meeting(meetname):
    _, meetings = get_meeting_adj(sanitize_name(meetname))
    if not meetings["prev"]:
        abort(404)
    return redirect(meetings["prev"]["slug"]["summary"], code=302)


@main.get("/")
def mainpage():
    return render_template("mainpage.html.j2")


@main.get("/about")
def aboutpage():
    return render_template("aboutpage.html.j2")


@socketio.on("connect")
def trigger_on_connect():
    global client_count
    client_count += 1
    logging.info("trigger_on_connect: client %s" % (client_count,))


@socketio.on("disconnect")
def trigger_on_disconnect():
    global client_count
    client_count -= 1
    logging.info("trigger_on_disconnect: client %s" % (client_count,))


@click.command()
@click.option("-p", "--portdata", "portdata", help="Set the port value [0-65536]", default="9696")
@click.option(
    "-6",
    "--ipprotv6",
    "netprotc",
    flag_value="ipprotv6",
    help="Start the server on an IPv6 address",
)
@click.option(
    "-4",
    "--ipprotv4",
    "netprotc",
    flag_value="ipprotv4",
    help="Start the server on an IPv4 address",
)
@click.version_option(version=__version__, prog_name="Fragment")
def mainfunc(portdata, netprotc):
    print(" * Starting Fragment...")
    print(" * Port number : " + str(portdata))
    netpdata = ""
    if netprotc == "ipprotv6":
        print(" * IP version  : 6")
        netpdata = "::"
    elif netprotc == "ipprotv4":
        print(" * IP version  : 4")
        netpdata = "0.0.0.0"
    main.config["TEMPLATES_AUTO_RELOAD"] = True
    main.run(port=portdata, host=netpdata)


@main.errorhandler(404)
def page_not_found(error):
    return render_template("e404page.html.j2"), 404


if __name__ == "__main__":
    socketio.run(mainfunc())
