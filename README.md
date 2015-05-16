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
