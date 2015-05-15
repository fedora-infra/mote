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
  templateSelection: formatResSelection,
  debug: true
});
