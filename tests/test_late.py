from utility import fake_datagrepper

import mote.modules.late


def test_fetch_recent_meetings_day(client, mocker):
    datagrepper = mocker.patch("urllib.request.urlopen", side_effect=fake_datagrepper)
    r, d = mote.modules.late.fetch_recent_meetings(1)

    datagrepper.assert_called_once()
    assert f"delta={mote.modules.late.seconds_delta * 1}" in datagrepper.call_args[0][0]
    assert "exception" not in d
    assert r is True
    assert len(d) == 2


def test_fetch_recent_meetings_week(client, mocker):
    datagrepper = mocker.patch("urllib.request.urlopen", side_effect=fake_datagrepper)
    r, d = mote.modules.late.fetch_recent_meetings(7)

    datagrepper.assert_called_once()
    assert f"delta={mote.modules.late.seconds_delta * 7}" in datagrepper.call_args[0][0]
    assert "exception" not in d
    assert r is True
    assert len(d) == 2
