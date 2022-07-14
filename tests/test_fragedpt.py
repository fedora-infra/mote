def test_fetch_channel(client):
    rv = client.get("/fragedpt/", query_string={"rqstdata": "listchan"})

    j = rv.get_json()
    assert len(j) > 0
    assert "fedora-meeting" in j


def test_fetch_channel_exc(client, mocker):
    listdir = mocker.patch("os.listdir")
    listdir.side_effect = Exception()
    rv = client.get("/fragedpt/", query_string={"rqstdata": "listchan"})

    j = rv.get_json()
    assert len(j) == 0


def test_fetch_channel_date(client):
    rv = client.get(
        "/fragedpt/",
        query_string={"rqstdata": "listdate", "channame": "fedora-meeting"},
    )

    j = rv.get_json()
    assert len(j) > 0
    assert "2020-06-10" in j


def test_fetch_channel_date_exc(client, mocker):
    listdir = mocker.patch("os.listdir")
    listdir.side_effect = Exception()
    rv = client.get(
        "/fragedpt/",
        query_string={"rqstdata": "listdate", "channame": "fedora-meeting"},
    )

    j = rv.get_json()
    assert len(j) == 0


def test_fetch_channel_meet(client):
    rv = client.get(
        "/fragedpt/",
        query_string={
            "rqstdata": "listmeet",
            "channame": "fedora-meeting",
            "datename": "2020-06-10",
        },
    )

    j = rv.get_json()
    assert len(j) > 0
    assert j[0]["channel"] == "fedora-meeting"
    assert j[0]["date"] == "Jun 10, 2020"
    assert j[0]["topic"] in ("fedora_iot_working_group_meeting", "magazine")


def test_fetch_channel_meet_exc(client, mocker):
    listdir = mocker.patch("os.listdir")
    listdir.side_effect = Exception()
    rv = client.get(
        "/fragedpt/",
        query_string={
            "rqstdata": "listmeet",
            "channame": "fedora-meeting",
            "datename": "2020-06-10",
        },
    )

    j = rv.get_json()
    assert len(j) == 0


def test_search_meeting(client):
    rv = client.get("/fragedpt/", query_string={"rqstdata": "srchmeet", "srchtext": "iot"})

    j = rv.get_json()
    assert len(j) > 0
    assert j[0]["channel"] == "fedora-meeting"
    assert j[0]["date"] == "Jun 10, 2020"
    assert j[0]["topic"] == "fedora_iot_working_group_meeting"


def test_search_meeting_exc(client, mocker):
    walk = mocker.patch("os.walk")
    walk.side_effect = Exception()
    rv = client.get("/fragedpt/", query_string={"rqstdata": "srchmeet", "srchtext": "iot"})

    j = rv.get_json()
    assert len(j) == 0


def test_search_non_existent_meeting(client):
    rv = client.get(
        "/fragedpt/",
        query_string={"rqstdata": "srchmeet", "srchtext": "non_existent_meeting"},
    )

    j = rv.get_json()
    assert len(j) == 0


def test_search_meeting_with_tgz(client):
    rv = client.get(
        "/fragedpt/",
        query_string={"rqstdata": "srchmeet", "srchtext": "test"},
    )

    j = rv.get_json()
    assert len(j) == 0


def test_fetch_last_week_meeting(client):
    rv = client.get("/fragedpt/", query_string={"rqstdata": "rcntlswk"})

    j = rv.get_json()
    assert isinstance(j, dict)


def test_fetch_last_week_meeting_exc(client, mocker):
    mocker.patch("urllib.request.urlopen", side_effect=Exception)
    rv = client.get("/fragedpt/", query_string={"rqstdata": "rcntlswk"})

    j = rv.get_json()
    assert isinstance(j, dict)
    assert len(j) == 0


def test_non_existing_parameters(client):
    rv = client.get("/fragedpt/", query_string={"rqstdata": "bleh"})

    j = rv.get_json()
    assert isinstance(j, dict)
    assert len(j) == 0


def test_get_calendar_events(client):
    rv = client.get(
        "/cal/events",
        query_string={
            "start": "2020-06-10T00:00:00",
            "end": "2020-06-17T00:00:00",
        },
    )

    j = rv.get_json()
    assert len(j) > 0
    assert "attendees" in j[0]
    assert "start" in j[0]
    assert "title" in j[0]
