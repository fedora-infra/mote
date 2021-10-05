"""
    Copyright (c) 2021 Fedora Websites and Apps

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import codecs
import os.path

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else '"'
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# setuptools configuration
setuptools.setup(
    name="mote",
    description="Python Flask project used to aggregate and distribute IRC meeting minutes and logs for the Fedora Project",
    long_description="Python Flask project used to aggregate and distribute IRC meeting minutes and logs for the Fedora Project",
    url="https://github.com/fedora-infra/mote",
    author="Fedora Websites and Apps Team",
    author_email="websites@lists.fedoraproject.org",
    maintainer="Akashdeep Dhar",
    maintainer_email="t0xic0der@fedoraproject.org",
    license="MIT",
    # extract version from source
    version=get_version("src/mote/__init__.py"),
    # tell distutils packages are under src directory
    package_dir={
        "": "src",
    },
    include_package_data=True,
    zip_safe=False,
    packages=setuptools.find_packages("src"),
    install_requires=["flask", "beautifulsoup4"],
    # automatically create console scripts
    entry_points={
        "console_scripts": [
            "start-mote-server=mote.main:mainfunc",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet",
    ],
)
