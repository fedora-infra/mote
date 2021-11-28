def test_non_existing_meeting(client):
    rv = client.get("/fedora-meeting/2020-06-10/bleh")
    assert b'<p class="h4 body">404 Not Found</p>' in rv.data
    assert rv.status_code == 404


def test_meeting_summary(client):
    rv = client.get(
        "/smry/fedora-meeting/2020-06-10/fedora_iot_working_group_meeting.2020-06-10-14.10.html"
    )
    assert b">Fedora IoT Working Group Meeting</span>" in rv.data


def test_meeting_minutes(client):
    rv = client.get(
        "/fedora-meeting/2020-06-10/fedora_iot_working_group_meeting.2020-06-10-14.10.html"
    )
    assert b"<h1>#fedora-meeting: Fedora IoT Working Group Meeting</h1>" in rv.data


def test_meeting_log(client):
    rv = client.get(
        "/fedora-meeting/2020-06-10/fedora_iot_working_group_meeting.2020-06-10-14.10.log.html"
    )
    assert b"Meeting started Wed Jun 10 14:10:12 2020 UTC." in rv.data


def test_meeting_txt(client):
    rv = client.get(
        "/fedora-meeting/2020-06-10/fedora_iot_working_group_meeting.2020-06-10-14.10.txt"
    )
    assert rv.status_code == 302


def test_meeting_log_txt(client):
    rv = client.get(
        "/fedora-meeting/2020-06-10/fedora_iot_working_group_meeting.2020-06-10-14.10.log.txt"
    )
    assert rv.status_code == 302
