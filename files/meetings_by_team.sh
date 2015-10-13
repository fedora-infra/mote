#!/bin/bash

# separates meetings by "team" from a single meeting channel folder, and 
# places them into separate folders for each team in the $BASELOCATION,
# which needs to be created prior to use

# "teams" are defined by #meetingname when starting a meeting

# edit file with appropriate paths and variables
# to use this script. 

# fedmsg_consumer.py references this file at /usr/local/bin/meetings_by_team.sh

BASELOCATION=/srv/web/meetbot/teams
cd $BASELOCATION
cd ..

for f in `find -type f -mtime -30 | grep -v "fedora-meeting\."`
do
    teamname=$(basename $f | awk -F. '{ print $1 }' )
    mkdir -p $BASELOCATION/$teamname
    ln -f -s $PWD/$f $BASELOCATION/$teamname/
done
