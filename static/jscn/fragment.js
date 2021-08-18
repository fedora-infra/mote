/*
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
*/

async function populate_channel_list() {
    document.getElementById("listchan-uols").innerHTML = "";
    document.getElementById("chanhead").innerHTML = "Loading...";
    await $.getJSON("/fragedpt/", {
        "rqstdata": "listchan"
    }, function (data) {
        for (let indx in data) {
            $("#listchan-uols").append(`
                <li class="list-group-item" type="button" data-bs-toggle="modal" data-bs-dismiss="modal" data-bs-target="#datemode" onclick="populate_datetxt_list('${indx}');">
                    <div class="head h4">${indx}</div>
                    <div class="body small"><span class="fw-bold">Source: </span><a href="${data[indx]}">${data[indx]}</a></div>
                </li>
            `);
        }
        document.getElementById("chanhead").innerHTML = "Channels";
    });
}

async function populate_datetxt_list(channel) {
    document.getElementById("listdate-uols").innerHTML = "";
    document.getElementById("datehead").innerHTML = "Loading...";
    await $.getJSON("/fragedpt/", {
        "rqstdata": "listdate",
        "channame": channel,
    }, function (data) {
        for (let indx in data) {
            $("#listdate-uols").append(`
                <li class="list-group-item" type="button" data-bs-toggle="modal" data-bs-dismiss="modal" data-bs-target="#meetmode" onclick="populate_meeting_list('${channel}', '${indx}');">
                    <div class="head h4">${indx}</div>
                    <div class="body small"><span class="fw-bold">Source: </span><a href="${data[indx]}">${data[indx]}</a></div>
                </li>
            `);
        }
        document.getElementById("datehead").innerHTML = "Meeting dates for " + channel;
    });
}

async function populate_meeting_list(channel, datetxt) {
    document.getElementById("listmeet-uols").innerHTML = "";
    document.getElementById("meethead").innerHTML = "Loading...";
    await $.getJSON("/fragedpt/", {
        "rqstdata": "listmeet",
        "channame": channel,
        "datename": datetxt
    }, function (data) {
        console.log(data);
        for (let indx in data) {
            $("#listmeet-uols").append(`
                <li class="list-group-item" type="button" data-bs-toggle="modal" data-bs-dismiss="modal" data-bs-target="#mainmode" onclick="render_meeting_logs_and_summary('${indx}', '${data[indx]['logs']}', '${data[indx]['summary']}');">
                    <div class="head h4">${indx}</div>
                    <div class="body small"><span class="fw-bold">Logs: </span><a href="${data[indx]['logs']}">${data[indx]['logs']}</a></div>
                    <div class="body small"><span class="fw-bold">Summary: </span><a href="${data[indx]['summary']}">${data[indx]['summary']}</a></div>
                </li>
            `);
        }
        document.getElementById("meethead").innerHTML = "Meetings on " + datetxt + " for " + channel;
    });
}

async function render_meeting_logs_and_summary(name, logslink, summlink) {
    document.getElementById("mainhead").innerHTML = "Loading...";
    document.getElementById("summ-cont").innerHTML = "";
    document.getElementById("logs-cont").innerHTML = "";
    await $.getJSON("/fragedpt/", {
        "rqstdata": "obtntext",
        "meetname": name,
        "summlink": summlink,
        "logslink": logslink
    },function (data) {
        console.log(data);
        document.getElementById("mainhead").innerText = data["meetname"];
        document.getElementById("summ-cont").innerHTML = data["summary_markup"]
        document.getElementById("logs-cont").innerHTML = data["logs_markup"];
    });
}
