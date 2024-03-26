# Mote 2.0 (Meetbot Logs 2.0)

Mote (or Meetbot Logs) is a web service that aggregates and distributes summaries, minutes and logs of meetings
that takes place in an [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) or 
[Matrix](https://en.wikipedia.org/wiki/Matrix_(protocol)) channel for the Fedora Project.

## Features

The web service has the following features

- Chronological lookup of meeting summaries, minutes and logs using an interactive calendar view
- Snappier loading up of content due to application-like interface and behaviour of the web service
- Channel-wise and date-wise distinction of meeting summaries, minutes and logs within modals
- Faster intuitive search of meeting summaries, minutes and logs using asynchronous fetching

## Dependencies

### Frontend

- [Bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [Bootstrap Dark Mode](https://vinorodrigues.github.io/bootstrap-dark-5/)
- [Easy QR Code 4](https://github.com/ushelp/EasyQRCodeJS)
- [Font Awesome 5](https://fontawesome.com)
- [FullCalendar 5](https://fullcalendar.io/)
- [jQuery 3](https://jquery.com/)
- [Socket.IO 4](https://socket.io/)

### Backend

- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Fedora Messaging 3](https://fedora-messaging.readthedocs.io/en/stable/)
- [Flask 2](https://flask.palletsprojects.com/)
- [Flask Caching 2](https://flask-caching.readthedocs.io/en/latest/)
- [Flask SocketIO 5](https://flask-socketio.readthedocs.io/en/latest/)
- [Gevent 21](http://www.gevent.org/)
- [Gunicorn 20](https://gunicorn.org/)
- [Redis 4](https://github.com/redis/redis-py)
- [Requests 2](https://requests.readthedocs.io/en/latest/)

### Development

- [Black 21](https://black.readthedocs.io/en/stable/)
- [Flake8 3](https://flake8.pycqa.org/en/latest/)
- [Isort 5](https://pycqa.github.io/isort/)
- [Poetry](https://python-poetry.org/)
- [Pytest 6](https://docs.pytest.org/en/7.1.x/)
- [Tox 3](https://tox.wiki/en/latest/index.html)

## Setup

### Preliminary setup

1. Fork the repository.
   ```
   https://github.com/fedora-infra/mote
   ```
2. Download the archive of meeting logs from the link below.
   ```
   https://mega.nz/file/cJYykbKA#jJozcnIG-WzwlYVQUXF25lqM5A8PNl2knQObQrSpOSk
   ```
3. Clone the forked repository to your local storage.
   ```
   $ git clone git@github.com:<username>/mote.git
   ```
4. Navigate into the cloned repository.
   ```
   $ cd mote
   ```
5. Depending on the kind of approach required, follow either of the below sections.

### Containerized setup

1. Install [Podman](https://podman.io/getting-started/installation) on Fedora Linux.
   ```
   $ sudo dnf install podman
   ```
2. Extract the previously downloaded archive of meeting logs in the directory of the cloned repository.
   ```
   $ tar -xzf meetbot.tar.gz
   ```
3. Build the container image.
   ```
   $ podman build -t mote .
   ```
4. Start the development server on an IPv4 address and on port 9696.
   ```
   $ podman run -it --rm -p 9696:9696 -v ./meetbot:/srv/web/meetbot:Z -v ./mote:/opt/app/mote:Z mote
   ```

### Native setup

1. Install [Python 3](https://www.python.org/), [Virtualenv](https://virtualenv.pypa.io/en/latest/) and [Poetry](https://python-poetry.org/) on Fedora Linux.
   ```
   $ sudo dnf install python3 python3-virtualenv poetry
   ```
2. Extract the previously downloaded archive of meeting logs in the `/srv/web` directory.
   ```
   $ sudo mkdir -p /srv/web
   $ sudo chown $USER /srv/web
   $ tar -xzf meetbot.tar.gz -C /srv/web
   ```
3. Create and activate the virtual environment.
   ```
   $ virtualenv venv
   $ source venv/bin/activate
   ```
4. Install the defined packages from the Python project configuration file.
   ```
   $ (venv) poetry install
   ```
5. Start the development server on an IPv4 address and on port 9696.
   ```
   $ (venv) mote -p 9696 -4
   ```

## Setup Guide for Mac Users

1. Install [Python 3](https://www.python.org/), [Virtualenv](https://virtualenv.pypa.io/en/latest/) and [Poetry](https://python-poetry.org/) on mac machine.
   ```
   $ brew install python@3 virtualenv poetry
   ```
2. Extract the previously downloaded archive of meeting logs in the `/srv/web` directory.
   ```
   $ mkdir -p /srv/web
   $ tar -xzf meetbot.tar.gz -C /srv/web
   ```
3. Create and activate the virtual environment.
   Navigate into the directory where you extracted the meeting logs.
Create and activate a virtual environment:
   ```
   $ cd /srv/web
   $ virtualenv venv
   $ source venv/bin/activate
   ```
4. Install the defined packages from the Python project configuration file.
   ```
   $ (venv) poetry install
   ```
5. Start the development server on an IPv4 address and on port 9696.
   ```
   $ (venv) mote -p 9696 -4
   ```

## Accessing

The project is be served on http://localhost:9696/ and with appropriate firewall rules, it should be accessible to the devices connected to the same network.

## Contributing

Folks can contribute to the project by the following means

- Writing [documentation](https://github.com/fedora-infra/mote/blob/main/README.md) to better explain the functionality and development of the web service
- Testing out the [newly staged versions](https://meetbot.stg.fedoraproject.org/) of the web service and reporting bugs on the [issue tracker](https://github.com/fedora-infra/mote/issues).
- Collaborating with the [Fedora Websites and Apps Team](https://docs.fedoraproject.org/en-US/websites/) to discuss about new features and advancements.
- Opening [pull requests](https://github.com/fedora-infra/mote/pulls) to the repository to address existing issues available on the [issue tracker](https://github.com/fedora-infra/mote/issues).
