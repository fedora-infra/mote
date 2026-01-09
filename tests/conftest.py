from shutil import copytree

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
    copytree("tests/meetbot", str(path), dirs_exist_ok=True)
    return str(path)
