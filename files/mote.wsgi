#-*- coding: utf-8 -*-

# The three lines below are required to run on EL6 as EL6 has
# two possible version of python-sqlalchemy and python-jinja2
# These lines make sure the application uses the correct version.
import __main__
__main__.__requires__ = ['jinja2 >= 2.4']
import pkg_resources

import os
#Set the environment variable pointing to the configuration file
os.environ['MOTE_CONFIG_FOLDER'] = '/etc/mote/'

# The following is only needed if you did not install mote
# as a python module (for example if you run it from a git clone).
# import sys
# sys.path.insert(0, '/path/to/mote/')


# The most import line to make the wsgi working
from mote import app as application
from mote import soke
# Generate cache and store in memcached
soke.run()
