#!/bin/sh

black --line-length=100 mote/ tests/
isort --profile=black mote/ tests/
flake8 --max-line-length=100 mote/ tests/
