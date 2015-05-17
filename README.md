# mote
møte - Fedora meetbot log wrangler

### About

møte allows the Fedora community to search and explore IRC meetings. 
More information on meetings can be found [here](https://fedoraproject.org/wiki/Meeting_channel?rd=Fedora_meeting_channel)

### Using møte

Dependencies: 
 - `memcached` (`sudo yum install memcached`)
 - `libmemcached`, `libmemcached-devel` (`sudo yum install libmemcached libmemcached-devel`)
 - Python 2.7.x

`pip` Dependencies:
 - Install using `pip install -r requirements.txt`

Running møte:
 - Edit `mote/config.py` with necessary information
 - Run `python runmote.py`

### Contribute to møte

You can contribute code or data. møte is in need of contributors to increase it's name association data pool. 
Some of the meeting groups' names are difficult to understand: for instance, the term `famna` may be unfamiliar to prospective ambassadors. To help add friendlier names and create a clear grouping of meeting groups, you can fork, edit, and send a pull request to the following data files:

https://github.com/fedora-infra/mote/blob/master/name_mappings.json

https://github.com/fedora-infra/mote/blob/master/category_mappings.json

