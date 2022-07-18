import pytest

from mote.modules.find import find_meetings_by_substring


def test_find_meetings_by_substring_1(client):
    r, d = find_meetings_by_substring("iot")

    assert "exception" not in d
    assert r is True
    assert len(d) == 1
    assert d[0]["channel"] == "fedora-meeting"
    assert d[0]["datetime"].startswith("2020-06-10T")
    assert d[0]["topic"] == "fedora_iot_working_group_meeting"


@pytest.mark.parametrize(
    ("search_string", "count"),
    (
        ("fedora", 1),
        ("meeting", 1),
        ("fedora-iot", 0),
        ("zine", 1),
        ("2020-06-10", 2),
        ("infra", 0),
        ("ŇŬƧݺ", 0),
    ),
)
def test_find_meetings_by_substring_2(client, search_string, count):
    r, d = find_meetings_by_substring(search_string)

    assert "exception" not in d
    assert r is True
    assert len(d) == count


def test_find_meetings_by_substring_exc(client, mocker):
    mocker.patch("os.walk", side_effect=Exception)
    r, d = find_meetings_by_substring("iot")

    assert "exception" in d
    assert r is False
