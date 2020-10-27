#!/bin/sh
#
# Simple script to update *both* sets of Python package dependencies in one go.
# If ReadTheDocs.org supports Pipenv one day and a `requirements.txt` file is
# no longer required, this script can be dropped with some changes to the
# `.readthedocs.yml` config.
#

pipenv update
pipenv lock --requirements > requirements.txt
