/*
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
*/

function closeOthers() {
    // $('.lev1').slideUp();
}
function openList(ln, close_all) {
    // $("#open-"+ln).css('display', 'initial');
    $("#open-"+ln).slideToggle();
}
function openLogModal(fname, prefix_ending) {
    $("#loading-icon").html("<i class='fa fa-cog fa-spin fa-3x'></i>");

    var data = {
        "group_type": current_group_type,
        "group_id": current_group_id,
        "date_stamp": current_date_stamp,
        "file_name": fname,
        "file_type": "log"
    };
    $.ajax({
      type: "GET",
      url: "/get_meeting_log",
      data: data,
      dataType: "html"
    }).done(function (res) {
        var modal = '\
        <div class="modal fade" id="SLModal" tabindex="-1" role="dialog" aria-labelledby="modal-label" aria-hidden="true">\
        <div class="modal-dialog">\
          <div class="modal-content">\
            <div class="modal-header">\
              <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>\
              <h4 class="modal-title inline" id="modalLabel">#{title}</h4>\
              <a target="_blank" class="btn btn-info btn-sm modal-button pull-right" href="#{permalink}">Permalink</a>\
            </div>\
            <div class="modal-body log-display">\
              #{body}\
            </div>\
            <div class="modal-footer">\
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
            </div>\
          </div>\
        </div>\
        </div>\
        ';
        var markup = res;
        var permalink =  prefix_ending + fname;
        modal = modal.replace("#{title}", "Meeting");
        modal = modal.replace("#{body}", markup);
        modal = modal.replace("#{permalink}", permalink);
        $('body').append(modal);
        $("#loading-icon").html("");
        $('#SLModal').modal();
        $( "body" ).delegate( "#SLModal", "hidden.bs.modal", function () {
            $('#SLModal').remove(); // Get rid of the modal so that users can see refreshed content
        });
    });
}
function showLogs(date_stamp) {
    window.current_date_stamp = date_stamp;
    // request logs through AJAX based on date and group
    // use variables current_group_id and current_group_type
    var data = {
        "group_id": current_group_id,
        "group_type": current_group_type,
        "date_stamp": date_stamp
    };
    $("#minlogs").html("<i class='fa fa-spinner fa-spin fa-4x'></i>");
    $.ajax({
      type: "GET",
      url: "/request_logs",
      data: data,
      success: function (res) {
          var minutes = res.minutes;
          var logs = res.logs;
          var minutes_markup = "<b>Minutes</b><br /><ul class='minlog-ul'>";
          var logs_markup = "<b>Logs</b><br /><ul class='minlog-ul'>";
          var link_prefix;
          var prefix_ending;

          if (current_group_type == "team") {
              prefix_ending = "/teams/" + current_group_id + "/";
              link_prefix = window.meetbot_location + prefix_ending;
          }
          else {
              prefix_ending = "/" + current_group_id + "/" + date_stamp + "/";
              link_prefix = window.meetbot_location + prefix_ending;
          }
          minutes.forEach(function (ele, ind, arr) {
              minutes_markup += "<li>"+ ele +"<br /><a class='btn btn-info hidden-xs btn-xs openLogModal' data-ele=\""+ ele +"\" data-pfixending=\""+ prefix_ending +"\">View</a>  <a target='_blank' class='btn btn-warning btn-xs' href='"+ link_prefix + ele +"'>Original</a> <a target='_blank' class='btn btn-success btn-xs' href='"+ prefix_ending + ele +"'>Permalink</a></li>";
          });
          logs.forEach(function (ele, ind, arr) {
              logs_markup += "<li>"+ ele +"<br /><a class='btn btn-info hidden-xs btn-xs openLogModal' data-ele=\""+ ele +"\" data-pfixending=\""+ prefix_ending +"\">View Log</a>  <a target='_blank' class='btn btn-warning btn-xs' href='"+ link_prefix + ele +"'>Original</a> <a target='_blank' class='btn btn-success btn-xs' href='"+ prefix_ending + ele +"'>Permalink</a></li>";
          });
          minutes_markup += "</ul>";
          logs_markup += "</ul>";
          concat_markup = minutes_markup + logs_markup;
          $("#minlogs").html(concat_markup);
      },
      dataType: "json"
    });
}
$(function () {
    $(".hid-list").hide();
    $(".meeting-day").click(function () {
        $(".meeting-day").removeClass("active");
        $(this).addClass("active");
    });
    $(".yearToggle").click(function () {
        var year = $(this).data("year");
        closeOthers();
        openList(year);
    });
    $(".monthToggle").click(function () {
        var yearMonth = $(this).data("month");
        openList(yearMonth);
    });
    $(".dayToggle").click(function () {
        var day = $(this).data("day");
        showLogs(day);
    });
    $("#showLatestMeeting").click(function () {
        var latestMeeting = $(this).data("latestmtg");
        showLogs(latestMeeting);
    });

    $("body").delegate(".openLogModal", "click", function () {
        var ele = $(this).data("ele");
        var pfixending = $(this).data("pfixending");
        openLogModal(ele, pfixending);
    });
});
