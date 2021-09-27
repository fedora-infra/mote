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

async function initialize_search_modal() {
    document.getElementById("find-body").innerHTML = `
        <div id="find-init">
            <div class="text-center mt-4">
                <i class="display-1 fas fa-search"></i>
            </div>
            <div class="h4 head text-center mt-2 mb-2">
                Search for conversations
            </div>
            <div class="small text-center mb-4">
                Enter a substring to begin looking for the conversations
            </div>
        </div>
        <div id="find-cont"></div>
        <div id="none-find"></div>
    `;
    document.getElementById("findtext").value = "";
}

async function search_meetings() {
    let srchtext = document.getElementById("findtext").value;
    document.getElementById("none-find").innerHTML = "";
    await $.getJSON("/fragedpt/", {
        "rqstdata": "srchmeet",
        "srchtext": srchtext
    }, function (data) {
        if (JSON.stringify(data) === JSON.stringify([]) || data.length === undefined) {
            document.getElementById("none-find").innerHTML = `
                <div class="text-center mt-4">
                    <i class="display-1 fas fa-comment-slash"></i>
                </div>
                <div class="h4 head text-center mt-2 mb-2">
                    Seems like there aren't any great matches for your search
                </div>
                <div class="small text-center mb-4">
                    Please modify your search string to better fit what you are looking for
                </div>
            `;
            document.getElementById("find-cont").innerHTML = "";
            document.getElementById("find-init").innerHTML = "";
        } else {
            document.getElementById("none-find").innerHTML = "";
            document.getElementById("find-cont").innerHTML = `
                <div class="text-center text-muted mt-1 mb-1">${data.length} conversation(s) found</div>
                <ul class="list-group" id="listfind-uols"></ul>
            `;
            document.getElementById("find-init").innerHTML = "";
            data = data.reverse();
            for (let indx in data) {
                $("#listfind-uols").append(`
                    <a class="list-group-item list-group-item-action" 
                       type="button" 
                       href="${data[indx]["slug"]["summary"]}" 
                       target="_blank">
                        <div class="head h4 mb-0 ellipsis">
                            <span>${data[indx]["topic"]}</span>
                        </div>
                        <div class="fst-italic small text-muted mt-1">
                            <i class="fas fa-clock"></i>&nbsp;${data[indx]["time"]}&nbsp;
                            <i class="fas fa-calendar"></i>&nbsp;${data[indx]["date"]}&nbsp;
                            <i class="fas fa-layer-group"></i>&nbsp;${data[indx]["channel"]}&nbsp;
                        </div>
                    </a>
                `);
            }
        }
    });
    document.getElementById("rcnthead").innerHTML = "Recent conversations";
}

async function populate_channel_list() {
    document.getElementById("listchan-uols").innerHTML = "";
    document.getElementById("chanhead").innerHTML = "Loading...";
    document.getElementById("chanfoot").innerHTML = `
        <span class="spinner-border spinner-border-sm mt-2" role="status" aria-hidden="true"></span>
    `;
    await $.getJSON("/fragedpt/", {
        "rqstdata": "listchan"
    }, function (data) {
        for (let indx in data) {
            $("#listchan-uols").append(`
                <li class="list-group-item list-group-item-action" 
                    type="button" 
                    data-bs-toggle="modal" 
                    data-bs-dismiss="modal" 
                    data-bs-target="#datemode" 
                    onclick="populate_datetxt_list('${indx}');">
                    <div class="head h4">${indx}</div>
                    <div class="body small">
                        <span class="fw-bold">Source: </span>
                        <a href="${data[indx]}" target="_blank">${data[indx]}</a>
                    </div>
                </li>
            `);
        }
        document.getElementById("chanhead").innerHTML = "Channels";
        document.getElementById("chanfoot").innerHTML = "Pick a channel of your choice";
    });
}

async function populate_datetxt_list(channel) {
    document.getElementById("listdate-uols").innerHTML = "";
    document.getElementById("datehead").innerHTML = "Loading...";
    document.getElementById("datefoot").innerHTML = `
        <span class="spinner-border spinner-border-sm mt-2" role="status" aria-hidden="true"></span>
    `;
    await $.getJSON("/fragedpt/", {
        "rqstdata": "listdate",
        "channame": channel,
    }, function (data) {
        const dataSorted = Object.entries(data);
        dataSorted.reverse();
        for (let i = 0; i < dataSorted.length; i++) {
            const element = dataSorted[i];
            const date = element[0];
            const url = element[1];
            $("#listdate-uols").append(`
                <li class="list-group-item list-group-item-action" 
                    type="button" 
                    data-bs-toggle="modal" 
                    data-bs-dismiss="modal" 
                    data-bs-target="#meetmode" 
                    onclick="populate_meeting_list('${channel}', '${date}');">
                    <div class="head h4">${date}</div>
                    <div class="body small">
                        <span class="fw-bold">Source: </span>
                        <a href="${url}" target="_blank">${url}</a>
                    </div>
                </li>
            `);
        }
        document.getElementById("datehead").innerHTML = "Meeting dates for " + channel;
        document.getElementById("datefoot").innerHTML = "Pick a date of your choice";
    });
}

async function populate_meeting_list(channel, datetxt) {
    document.getElementById("listmeet-uols").innerHTML = "";
    document.getElementById("meethead").innerHTML = "Loading...";
    document.getElementById("meetfoot").innerHTML = `
        <span class="spinner-border spinner-border-sm mt-2" role="status" aria-hidden="true"></span>
    `;
    await $.getJSON("/fragedpt/", {
        "rqstdata": "listmeet",
        "channame": channel,
        "datename": datetxt
    }, function (data) {
        for (let indx in data) {
            $("#listmeet-uols").append(`
                <a class="list-group-item list-group-item-action"
                    type="button" 
                    href="${data[indx]["slug"]["summary"]}" 
                    target="_blank">
                    <div class="head h4 mb-0 ellipsis">
                        <span>${data[indx]["topic"]}</span>
                    </div>
                    <div class="fst-italic small text-muted mt-1">
                        <i class="fas fa-clock"></i>&nbsp;${data[indx]["time"]}&nbsp;
                        <i class="fas fa-calendar"></i>&nbsp;${data[indx]["date"]}&nbsp;
                        <i class="fas fa-layer-group"></i>&nbsp;${data[indx]["channel"]}&nbsp;
                    </div>
                </a>
            `);
        }
        document.getElementById("meethead").innerHTML = "Meetings on " + datetxt + " for " + channel;
        document.getElementById("meetfoot").innerHTML = "Pick a meeting of your choice";
    });
}

async function populate_recent_meeting_list() {
    document.getElementById("listrcnt-daya-uols").innerHTML = "";
    document.getElementById("listrcnt-week-uols").innerHTML = "";
    document.getElementById("none-daya").innerHTML = "";
    document.getElementById("none-week").innerHTML = "";
    document.getElementById("rcnthead").innerHTML = "Loading...";
    await $.getJSON("/fragedpt/", {
        "rqstdata": "rcntlsdy"
    }, function (data) {
        populate_recent_meeting_on_dom(data, "daya");
    });
    await $.getJSON("/fragedpt/", {
        "rqstdata": "rcntlswk"
    }, function (data) {
        populate_recent_meeting_on_dom(data, "week");
    });
    document.getElementById("rcnthead").innerHTML = "Recent conversations";
}

function populate_recent_meeting_on_dom(data, tabtitle) {
    if (JSON.stringify(data) === JSON.stringify({})) {
        document.getElementById("none-" + tabtitle).innerHTML = `
            <div class="text-center mt-4">
                <i class="display-1 fas fa-comment-slash"></i>
            </div>
            <div class="h4 head text-center mt-2 mb-2">
                Seems like everyone's keeping quiet
            </div>
            <div class="small text-center mb-4">
                Please come back later to get more recent meetings
            </div>
        `;
    } else {
        for (let indx in data) {
            $("#listrcnt-" + tabtitle + "-uols").append(`
                <a class="list-group-item list-group-item-action" 
                   type="button" 
                   href="${data[indx]["slug"]["summary"]}" 
                   target="_blank">
                    <div class="head h4 mb-0 ellipsis">
                        <span>${data[indx]["topic"]}</span>
                    </div>
                    <div class="fst-italic small text-muted mt-1">
                        <i class="fas fa-clock"></i>&nbsp;${data[indx]["time"]}&nbsp;
                        <i class="fas fa-layer-group"></i>&nbsp;${data[indx]["channel"]}&nbsp;
                    </div>
                </a>
            `);
        }
    }
}
