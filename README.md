# Mote 2.0

Python Flask project used to aggregate and distribute IRC meeting minutes and logs for the Fedora Project

## How to set up a local development environment?

1. Download the meeting archive https://mega.nz/file/cJYykbKA#jJozcnIG-WzwlYVQUXF25lqM5A8PNl2knQObQrSpOSk.
2. Extract the contents to `/srv/web/meetbot` directory. 
3. `git clone https://github.com/fedora-infra/mote.git`
4. `cd mote/`
5. `virtualenv venv`
6. `source venv/bin/activate`
7. `python3 setup.py install`
8. `start-mote-server --help`
9. `start-mote-server -p 9696 -4`

Detailed documentation would arrive shortly. Inconvenience is regretted.
