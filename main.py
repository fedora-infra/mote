"""
##########################################################################
*
*   Copyright © 2019-2021 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

import click
from flask import Flask, \
    render_template, \
    request, \
    jsonify, \
    abort
from call import fetch_channel_dict, \
    fetch_datetxt_dict, \
    fetch_meeting_dict, \
    fetch_meeting_content, \
    fetch_meeting_logs_and_summary


main = Flask(__name__)


@main.get("/fragedpt/")
def fragedpt():
    rqstdata = request.args.get("rqstdata")
    response = {}
    if rqstdata == "listchan":
        chanobjc = fetch_channel_dict()
        if chanobjc[0]:
            response = chanobjc[1]
        else:
            print("Channel list could not be retrieved")
    elif rqstdata == "listdate":
        channame = request.args.get("channame")
        dateobjc = fetch_datetxt_dict(channame)
        if dateobjc[0]:
            response = dateobjc[1]
        else:
            print("Date list could not be retrieved")
    elif rqstdata == "listmeet":
        channame = request.args.get("channame")
        datename = request.args.get("datename")
        meetobjc = fetch_meeting_dict(channame, datename)
        if meetobjc[0]:
            response = meetobjc[1]
        else:
            print("Meeting list could not be retrieved")
    elif rqstdata == "obtntext":
        summlink = request.args.get("summlink")
        logslink = request.args.get("logslink")
        obtndata = fetch_meeting_logs_and_summary(summlink, logslink)
        if obtndata[0]:
            response = obtndata[1]
        else:
            print("Meeting summary and logs could not be retrieved")
    return jsonify(response)


@main.get("/<channame>/<cldrdate>/<meetname>/")
def statfile(channame, cldrdate, meetname):
    meetname = meetname.replace(".log.html", "").replace(".html", "")
    meetpath = "https://meetbot-raw.fedoraproject.org" + request.path
    if meetpath[-1] == "/":
        meetpath = meetpath[0:-1]
    meetcont = fetch_meeting_content(meetpath)
    if meetcont[0]:
        if ".log.html" in request.path:
            typecont = "Logs"
        elif ".html" in request.path:
            typecont = "Minutes"
        else:
            typecont = "Contents"
        return render_template("statfile.html",
                               channame=channame,
                               cldrdate=cldrdate,
                               meetname=meetname,
                               typecont=typecont,
                               meetcont=meetcont[1])
    else:
        abort(404)


@main.get("/")
def mainpage():
    return render_template("mainpage.html")


@click.command()
@click.option("-p", "--portdata", "portdata", help="Set the port value [0-65536]", default="9696")
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address")
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address")
@click.version_option(version="0.1.0", prog_name="Fragment")
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


if __name__ == "__main__":
    mainfunc()@click.command()
