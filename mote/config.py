'''
Database Configuration
'''
# DB Type: ["mysql", "postgresql"]
dbtype = "mysql"

dbhost = "localhost"
dbuser = "root"
dbpass = "root"
dbname = "mote"

'''
Scraper Configuration
'''

# log_endpoint = "http://meetbot.fedoraproject.org"
log_endpoint = "/srv/web/zodbot"

# Fedora has a "teams" folder which contains
# logs from meetings started with a certain team name
# for instance, `#startmeeting famna` will save in "teams/famna"
# Folders not in "teams" reflect the channel name of the meeting
log_team_folder = "teams"

# Directories to ignore in crawling the logs.
# These folders are ignored. The "meetbot" folder is
# an infinite loop on Fedora's meetbot.
# This should probably be fixed.
ignore_dir = ["teams", "meetbot"]
