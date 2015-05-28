# -*- coding: utf-8 -*-
#
# Copyright © 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='mote',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1a1',

    description="""møte is a Fedora IRC meeting log wrangler,
    allowing users to employ an easy-to-use web front to explore the Fedora Project's
    regular meetings.""",

    # The project's main homepage.
    url='https://github.com/fedora-infra/mote',

    # Author details
    author='Chaoyi Zha',
    author_email='cydrobolt@fedoraproject.org',
    # License
    license='GPLv2+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='irc meetbot fedora web scraper log',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Flask==0.10.1',
        'Jinja2==2.7.3',
        'MarkupSafe==0.23',
        'Werkzeug==0.10.4',
        'beautifulsoup4==4.3.2',
        'itsdangerous==0.24',
        'kitchen==1.2.1',
        'munch==2.0.2',
        'python-dateutil==2.4.2',
        'python-fedora==0.4.0',
        'python-memcached==1.54',
        'python-openid==2.2.5',
        'python-openid-cla==1.0',
        'python-openid-teams==1.0',
        'requests==2.7.0',
        'six==1.9.0',
        'urllib3==1.10.4',
        'wsgiref==0.1.2',
    ],

    include_package_data=True,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'mote=runmote:main',
        ],
    },
)
