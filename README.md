# møte
møte - Fedora meetbot log wrangler

[![](https://travis-ci.org/fedora-infra/mote.svg)](https://travis-ci.org/fedora-infra/mote)

[__Staging__](https://meetbot.stg.fedoraproject.org) | [__Production__](https://meetbot.fedoraproject.org)

### About

møte is an interface to MeetBot logs that allows the Fedora community to search and explore IRC meetings.
More information on meetings can be found [here](https://fedoraproject.org/wiki/Meeting_channel).

møte organises and serves meetings as a drop-in replacement, without needing any modification to the MeetBot plugin itself.

### Using møte

Dependencies:
 - Optional: `memcached` (`sudo dnf install memcached`)
 - Python 2.7.x (`sudo dnf install python2`) (Should install Python 2.17.13)

Installation:
 - Optional: create virtual environment
 - `pip install -r requirements.txt`
 - Install using `python setup.py develop`

Running møte:
 - Edit [config.py](./files/config.py) with necessary information and place the `config.py` in [`mote/`](./mote)
 - Run `python runmote.py`

Running tests:
 - `sh run_tests.sh`

### Contribute to møte

You can contribute code or data. møte is in need of contributors to increase its name association data pool.
Some of the meeting groups' names are difficult to understand: for instance, the term `famna` may be unfamiliar to prospective ambassadors. To help add friendlier names and create a clear grouping of meeting groups, you can fork, edit, and send a pull request to the following data files:

 - [name_mappings](./name_mappings.json)
 - [category_mappings](./category_mappings.json)
