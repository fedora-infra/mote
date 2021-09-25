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

import json
import os

directory_path = os.path.dirname("/srv/web/meetbot/")


def find_meetings_by_substring(search_string:str):
	"""
	Return list of meetings returned from search
	"""
	try:
		meeting_dictionary = []
		for root, dirs, files in os.walk(directory_path):
			for file in files:
				if search_string in file and not file.endswith(".tgz"):
					location = "%s/%s" % (root, str(file))
					if "/srv/web/meetbot/teams/" not in location:
						location_list = location.replace("/srv/web/meetbot/", "").split("/")
						channel_name, meeting_date, meeting_filename = location_list[0], location_list[1], location_list[2]
						if ".log.html" in meeting_filename:
							meeting_log_filename = meeting_filename
							meeting_summary_filename = meeting_filename.replace(".log.html", ".html")
							meeting_title = meeting_filename.replace(".log.html", "")
							meeting_object = {
								"meeting_topic": meeting_title,
								"channel": channel_name,
								"time": meeting_date,
								"url": {
									"logs": "https://meetbot-raw.fedoraproject.org/%s/%s/%s" % (channel_name, meeting_date, meeting_log_filename),
									"summary": "https://meetbot-raw.fedoraproject.org/%s/%s/%s" % (channel_name, meeting_date, meeting_summary_filename),
								}
							}
							meeting_dictionary.append(meeting_object)
		return True, meeting_dictionary
	except Exception as expt:
		return False, {"exception": str(expt)}


if __name__ == "__main__":
	print(json.dumps(find_meetings_by_substring(input()), indent=4))
