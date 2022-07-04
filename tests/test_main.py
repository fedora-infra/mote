from click.testing import CliRunner

import mote.main


def test_root(client):
    rv = client.get("/")
    assert b"<title>Meetbot Logs</title>" in rv.data


def test_mainfunc(mocker):
    run = mocker.patch("mote.main.main.run", return_value=True)
    cli = CliRunner()
    rv = cli.invoke(mote.main.mainfunc)
    run.assert_called_once()

    rv = cli.invoke(mote.main.mainfunc, ["-p", "12345"])
    assert "Port number : 12345" in rv.output
    rv = cli.invoke(mote.main.mainfunc, ["-4"])
    assert "IP version  : 4" in rv.output
    rv = cli.invoke(mote.main.mainfunc, ["-6"])
    assert "IP version  : 6" in rv.output

    assert run.call_count == 4
