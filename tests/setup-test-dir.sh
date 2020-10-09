#!/bin/bash
# Set up a few files for testing in a directory.
# The config file is in .../config/.

set -e

DIR="$1"
[ -n "$DIR" ]

DATA="$DIR/meetbot_data"

mkdir -vp $DIR/config
cat $(dirname $0)/../files/test_config.py >$DIR/config/config.py

cp $(dirname $0)/../{category,name}_mappings.json $DIR/

mkdir -vp $DATA
mkdir -p $DATA/fedora-meeting-1/2014-02-04
mkdir -p $DATA/fedora-meeting/2014-02-04
mkdir -p $DATA/teams/team_one

touch $DATA/fedora-meeting-1/2014-02-04/fedora-meeting-1.2014-02-04-20.11.html
touch $DATA/fedora-meeting/2014-02-04/fedora-meeting.2014-02-04-20.11.html

touch $DATA/teams/team_one/team_one.2014-02-04-20.11.html
touch $DATA/teams/team_one/team_one.2014-02-04-20.11.log.html
