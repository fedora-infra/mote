Thanks for your interest in contributing to Fedora møte. Your efforts are greatly appreciated.

Quickstart:

  1. Scan through the current [issues] (https://github.com/fedora-infra/mote/issues) to find one that interests you.
  2. You can also create a [new issue](https://github.com/fedora-infra/mote/issues/new) to work on.
  3. Fork from the [GitHub repository](https://github.com/fedora-infra/mote).
  4. Fix the bug or add the feature, write tests to show bug fix or working feature.
  5. Submit a pull request and wait for a review from maintainers.

# Development Environment

## Dependencies:
 - [`memcached`](https://memcached.org) (`sudo dnf install memcached`)
 - Python 3.8.x
 - [Pipenv](https://docs.pipenv.org/) (`sudo dnf install pipenv`)

## Virtual Environment setup:
 - `pipenv install` will create a new virtual environment and install the requirements.
 - `pipenv shell` will activate Python's virtual environement's shell.

## Running møte:
 - Start `memcached` by typing `memcached` in the terminal and pressing Return (Enter) key.
 - Edit [config.py](./files/config.py) with necessary information and place the `config.py` in [`mote/`](./mote)
 - Modify the copied `config.py` to use memcached by setting `use_memcached = TRUE`
   - You can do it by running the following command in command line too: `sed -i '/use_memcached = / s/False/True/' mote/config.py`
 - Enter the Pipenv's newly created virtualenv's shell with `pipenv shell`
 - Run `python runmote.py`

**Note :** Make sure `memcached` is running in the background.

## Running tests:
 - `sh run_tests.sh`
 
 # Organizing Meeting Groups
 
 Naming of some of the meeting groups are difficult to understand. For instance, the term `famna` may be unfamiliar to prospective ambassadors. To help add friendlier names and create clear meeting groups, you can fork, edit, and send a pull request to the following data files:

 - [name_mappings](./name_mappings.json)
 - [category_mappings](./category_mappings.json)




