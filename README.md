# Mote 2.0

Python Flask project used to aggregate and distribute IRC meeting minutes and logs for the Fedora Project.

## Description

The project can be described as follows

- Mote is a web application purposed to aggregate and distribute the minutes and logs for IRC/Matrix meetings of the Fedora Project community.
- The project allows looking up meeting info with channel names, dates/times of occurrence and lists recent meetings for quick access.
- The backend is written in Python with the use of libraries such as Flask micro web framework, BeautifulSoup4, Urllib3, Click, Werkzeug etc.
- The frontend is written in HTML5, CSS3 and ES6 with the use of libraries such as Bootstrap 5, jQuery, Popper.JS, EasyQRCode etc.

## View Project

Click [this link](https://meetbot.fedoraproject.org/) to view the project.

## Setting up a local development environment

You can download the meeting log archive from the link below

```
https://mega.nz/file/cJYykbKA#jJozcnIG-WzwlYVQUXF25lqM5A8PNl2knQObQrSpOSk
```

1. Clone the repository
   ```
   git clone https://github.com/fedora-infra/mote.git
   ```
2. Navigate to the cloned repository
   ```
   cd mote
   ```

### There are two ways to set up this project

#### Containerized setup

3. Install [Podman](https://podman.io/getting-started/installation) (require root privileges) on Fedora
   ```
   sudo dnf install podman
   ```
4. Extract the meetbot archive
   ```
   tar xzf meetbot.tar.gz
   ```
5. Build the container image
   ```
   podman build -t mote .
   ```
6. Run the server
   ```
   podman run -it --rm -p 9696:9696 -v ./meetbot:/srv/web/meetbot:Z mote
   ```

**Congratulations!** The project is being served on http://localhost:9696.

#### Native setup

Mote expects to find meeting logs in `/srv/web/meetbot`.

3. Extract the meetbot archive in `/srv/web` (requires root privileges)
   ```
   sudo mkdir -p /srv/web
   sudo chown $USER /srv/web
   tar xzf meetbot.tar.gz -C /srv/web
   ```
4. Create a dedicated virtual environment
   ```
   python3 -m venv venv
   ```
5. Activate the virtualenv
   ```
   source venv/bin/activate
   ```
6. Install Poetry usig pip package manager.
   ```
   pip install poetry
   ```
7. Install the defined dependencies from lock file using Poetry  
   The dependencies of this project can be found in `pyproject.toml` and are installed using Poetry
   ```
   poetry install
   ```
8. Create a package in source as well as wheel format using Poetry
   ```
   poetry build
   ```
9. Run mote server
   ```
   mote
   ```

The project is served on http://localhost:9696/

For any help with this format, please run

```
mote --help
```

## Contributing

If you'd like to contribute to this project, you can look at existing issues and fill Pull Requests.  
You can also connect with the team at [#websites:fedoraproject.org](https://chat.fedoraproject.org/#/room/#websites:fedoraproject.org).
