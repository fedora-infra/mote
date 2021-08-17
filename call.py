import bs4 as btsp
import urllib.request as ulrq


def fetch_channel_dict():
    try:
        source = ulrq.urlopen("https://meetbot-raw.fedoraproject.org/").read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        channel_dict = {}
        for channel in parse_object.find_all("a")[5:]:
            channel_dict[channel.string[0:-1]] = channel.get("href")
        return channel_dict
    except Exception as expt:
        return None


def fetch_datetxt_dict(channel: str):
    try:
        source = ulrq.urlopen("https://meetbot-raw.fedoraproject.org/" + channel).read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        datetxt_dict = {}
        for datetxt in parse_object.find_all("a")[5:]:
            datetxt_dict[datetxt.string[0:-1]] = datetxt.get("href")
        return datetxt_dict
    except Exception as expt:
        return None


def fetch_meeting_dict(channel: str, datetxt: str):
    try:
        source = ulrq.urlopen("https://meetbot-raw.fedoraproject.org/" + channel + "/" + datetxt + "/").read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        meeting_dict = {}
        for meeting in parse_object.find_all("a")[5:]:
            if ".log.html" in meeting.string:
                meeting_log = meeting.string
                meeting_sum = meeting.string.replace(".log.html", ".html")
                meeting_key = meeting.string.replace(channel + ".", "").replace(datetxt + "-", "").replace(".log.html", "")
                meeting_dict[meeting_key] = {
                    "logs": meeting_log,
                    "summary": meeting_sum
                }
        return meeting_dict
    except Exception as expt:
        return None


if __name__ == "__main__":
    print(fetch_channel_dict())
    print(fetch_datetxt_dict("allegheny"))
    print(fetch_meeting_dict("allegheny", "2010-04-08"))
