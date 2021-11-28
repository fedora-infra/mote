from distutils import dir_util

import pytest

import mote.main
from mote import cache


@pytest.fixture
def client(meetbot_data):
    mote.main.main.config["TESTING"] = True
    mote.main.main.config["MEETING_DIR"] = meetbot_data
    with mote.main.main.app_context():
        with mote.main.main.test_client() as client:
            yield client
        cache.clear()


@pytest.fixture(scope="session")
def meetbot_data(tmpdir_factory):
    path = tmpdir_factory.mktemp("meetbot")
    dir_util.copy_tree("tests/meetbot", str(path))
    return str(path)
