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
 - `memcached` (`sudo dnf install memcached`)
 - Python 3.8.X
 - Pipenv

Installation:
 - `pipenv install` will create a new virtual environment and install the requirements. `

Running møte:
 - Start `memcached` by typing `memcached` in the terminal and pressing Return (Enter) key.
 - Edit [config.py](./files/config.py) with necessary information and place the `config.py` in [`mote/`](./mote)
 - Modify the copied `config.py` to use memcached by setting `use_memcached = TRUE`
   - You can do it by running the following command in command line too: `sed -i '/use_memcached = / s/False/True/' mote/config.py`
 - Enter the Pipenv's newly created virtualenv's shell with `pipenv shell`
 - Run `python runmote.py`

**Note :** Make sure `memcached` is running in the background.

Running tests:
 - `sh run_tests.sh`

### Contribute to møte

You can contribute code or data. møte is in need of contributors to increase its name association data pool.
Some of the meeting groups' names are difficult to understand: for instance, the term `famna` may be unfamiliar to prospective ambassadors. To help add friendlier names and create a clear grouping of meeting groups, you can fork, edit, and send a pull request to the following data files:

 - [name_mappings](./name_mappings.json)
 - [category_mappings](./category_mappings.json)
