'''
Scraper Configuration
'''

log_endpoint = "/srv/web/meetbot"
# log_endpoint = "/home/user/mote/test_data/meetbot"

# Fedora has a "teams" folder which contains
# logs from meetings started with a certain team name
# for instance, `#startmeeting famna` will save in "teams/famna"
# Folders not in "teams" reflect the channel name of the meeting
log_team_folder = "teams"

# Directories to ignore in crawling the logs.
# These folders are ignored. The "meetbot" folder is
# an infinite loop on Fedora's meetbot.
# This should probably be fixed. This should probably be
# an array, but...
ignore_dir = "meetbot"

# Location where logs are stored (remote location)
meetbot_prefix = "http://meetbot.fedoraproject.org"

'''
General Configuration
'''
enable_debug = True
app_port = 5000
app_host = "127.0.0.1"
admin_groups = ["sysadmin-mote"]
