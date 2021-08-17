import click
from flask import Flask, render_template


main = Flask(__name__)


@main.get("/")
def mainpage():
    return render_template("mainpage.html")


@click.command()
@click.option("-p", "--portdata", "portdata", help="Set the port value [0-65536]", default="9696")
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address")
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address")
@click.version_option(version="0.1.0", prog_name="Fragment")
def mainfunc(portdata, netprotc):
    print(" * Starting Fragment...")
    print(" * Port number : " + str(portdata))
    netpdata = ""
    if netprotc == "ipprotv6":
        print(" * IP version  : 6")
        netpdata = "::"
    elif netprotc == "ipprotv4":
        print(" * IP version  : 4")
        netpdata = "0.0.0.0"
    main.config["TEMPLATES_AUTO_RELOAD"] = True
    main.run(port=portdata, host=netpdata)


if __name__ == "__main__":
    mainfunc()@click.command()