/*
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
*/

var $eventSelect = $(".tpa");

function formatRes (res) {
    if (res.loading) return res.text;

    var markup = '<div class="clearfix">' +
    '<div>' +
    '<h4>' + res.name + '</h4>' +
    '<b>type: </b>' + res.type +
    '</div>' +
    '</div>';

    if (res.description) {
      markup += '<div>' + res.description + '</div>';
    }
    return markup;
}

function formatResSelection (res) {
    return res.name;
}

$(".tpa").select2({
  ajax: {
    url: "/search_sugg",
    dataType: 'json',
    delay: 250,
    data: function (params) {
      return {
        q: params.term, // search term
      };
    },
    processResults: function (data, page) {
      // parse the results into the format expected by Select2.
      // since we are using custom formatting functions we do not need to
      // alter the remote JSON data
      return {
        results: data.items
      };
    },
    cache: true
  },
  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
  minimumInputLength: 1,
  templateResult: formatRes,
  templateSelection: formatResSelection
});
function redirectResults (group_id, type) {
    window.location = "/sresults?group_id=" + group_id + "&type=" + type;
}
function closeOthers() {
    // $('.lev1').slideUp();
}
function openList(ln, close_all) {
    // $("#open-"+ln).css('display', 'initial');
    $("#open-"+ln).slideToggle();
}
function openLogModal(fname) {
    // type == minutes or logs
    var data = {
        "group_type": current_group_type,
        "group_id": current_group_id,
        "date_stamp": current_date_stamp,
        "file_name": fname,
    };
    $.ajax({
      type: "POST",
      url: "/get_meeting_log",
      data: data,
      dataType: "html"
    }).done(function (res) {
        console.log(res);
      var modal = '\
      <div class="modal fade" id="SLModal" tabindex="-1" role="dialog" aria-labelledby="modal-label" aria-hidden="true">\
        <div class="modal-dialog">\
          <div class="modal-content">\
            <div class="modal-header">\
              <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>\
              <h4 class="modal-title" id="modalLabel">#{title}</h4>\
            </div>\
            <div class="modal-body">\
              #{body}\
            </div>\
            <div class="modal-footer">\
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
            </div>\
          </div>\
        </div>\
      </div>\
      ';
      var markup;
      console.log(res);
      markup = res;
      modal = modal.replace("#{title}", "Meeting");
      modal = modal.replace("#{body}", markup);
      $('body').append(modal);
      $('#SLModal').modal();
      $( "body" ).delegate( "#SLModal", "hidden.bs.modal", function () {
            $('#SLModal').remove(); // Get rid of the modal so that users can see refreshed content
      });

      return true;
    });
    return true;
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
    $("#minlogs").html("<i class='fa fa-spinner fa-4x fa-spin'></i>");
    $.ajax({
      type: "POST",
      url: "/request_logs",
      data: data,
      success: function (res) {
          var minutes = res.minutes;
          var logs = res.logs;
          var minutes_markup = "<b>Minutes</b><br /><ul class='minlog-ul'>";
          var logs_markup = "<b>Logs</b><br /><ul class='minlog-ul'>";
          var link_prefix;
          if (current_group_type == "team") {
              link_prefix = "http://meetbot.fedoraproject.org/teams/" + current_group_id + "/";
          }
          else {
              link_prefix = "http://meetbot.fedoraproject.org/" + current_group_id + "/" + date_stamp + "/";
          }
          minutes.forEach(function (ele, ind, arr) {
              minutes_markup += "<li>"+ ele +"<br /><a class='btn btn-info btn-xs' href='javascript:void();' onclick=\"openLogModal('"+ ele +"');\">View Log</a>  <a class='btn btn-warning btn-xs' href='"+ link_prefix + ele +"'>Direct Link</a></li>";
          });
          logs.forEach(function (ele, ind, arr) {
              logs_markup += "<li>"+ ele +"<br /><a class='btn btn-info btn-xs' href='javascript:void();' onclick=\"openLogModal('"+ ele +"');\">View Log</a>  <a class='btn btn-warning btn-xs' href='"+ link_prefix + ele +"'>Direct Link</a></li>";
          });
          minutes_markup += "</ul>";
          logs_markup += "</ul>";
          concat_markup = minutes_markup + logs_markup;
          $("#minlogs").html(concat_markup);
      },
      dataType: "json"
    });
}

$eventSelect.on("select2:select", function (e) {
    group_id = e.params.data.id;
    group_type = e.params.data.type;
    if (auto_search === true) {
        redirectResults(group_id, group_type);
    }
    else {
        window.group_id = group_id;
        window.group_type = group_type;
    }
});

$("#search").click(function () {
    redirectResults(group_id, group_type);
});
$(function () {
    $(".hid-list").hide();
});
