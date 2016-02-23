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

function loadLogContents() {
    // type == minutes or logs
    var data = {
        "group_type": current_group_type,
        "group_id": current_group_id,
        "date_stamp": current_date_stamp,
        "file_name": current_fname,
    };
    $.ajax({
      type: "GET",
      url: "/get_meeting_log",
      data: data,
      dataType: "html"
  }).done(function (markup) {
        $('.logdisplay').html(markup);

        var container = $('.wrapper');
        var lineNum = location.hash.split('-')[1];

 	    var line = $('[name="l-' + lineNum + '"]').next();

        $('body').animate({
             scrollTop: line.offset().top - container.offset().top + container.scrollTop()
        });
    });
}

$(function () {
    loadLogContents();
    if (window.current_log_type == "minutes") {
        $(".logdisplay").addClass("single-log-minutes");
    }
});
