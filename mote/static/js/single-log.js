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

    if (window.current_log_type == "minutes") {
        $(".log-display").addClass("single-log-minutes");
    }

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
    }).done(function(markup) {
        $('.log-display').html(markup);

        var container = $('.wrapper');
        var lineNum = location.hash.split('-')[1];

        var line = $('[name="l-' + lineNum + '"]').next();

        try {
            $('body').animate({
                scrollTop: line.offset().top - container.offset().top + container.scrollTop()
            });
        } catch (e) {
            console.log("No line specified. Not scrolling.");
        }
    });
}

$(function() {
    if (window.current_log_type != 'meeting') {
        loadLogContents();
    }

    $('.select-meeting-type').click(function () {
        // if the log type is 'meeting', load the log
        // only after the user makes their selection

        $('.display-container').show();
        var new_log_type = $(this).data('mtype');

        window.current_log_type = new_log_type;

        // trim off .mtg
        var new_fname = window.current_fname.slice(0, -3);
        // add new extension
        console.log(current_log_type);
        new_fname += window.log_extensions[window.current_log_type];

        window.current_fname = new_fname;
        loadLogContents();

        $('.select-meeting-type-container').slideUp();
    });

});
