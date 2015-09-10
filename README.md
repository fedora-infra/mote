# møte
møte - Fedora meetbot log wrangler

[__Staging__](https://meetbot.stg.fedoraproject.org) | [__Production__](https://meetbot.fedoraproject.org)

### About

møte allows the Fedora community to search and explore IRC meetings.
More information on meetings can be found [here](https://fedoraproject.org/wiki/Meeting_channel)

### Using møte

Dependencies:
 - Optional: `memcached` (`sudo yum install memcached`)
 - Python 2.7.x

`pip` Dependencies:
 - Install using `python setup.py develop`

Running møte:
 - Edit `files/config.py` with necessary information and place `config.py` in `mote/config.py`
 - Run `python runmote.py`

### Contribute to møte

You can contribute code or data. møte is in need of contributors to increase its name association data pool.
Some of the meeting groups' names are difficult to understand: for instance, the term `famna` may be unfamiliar to prospective ambassadors. To help add friendlier names and create a clear grouping of meeting groups, you can fork, edit, and send a pull request to the following data files:

 - [name_mapping](https://github.com/fedora-infra/mote/blob/master/name_mappings.json)
 - [category_mappings](https://github.com/fedora-infra/mote/blob/master/category_mappings.json)
