# fragment
Python Flask project used to aggregate and distribute IRC meeting minutes and logs for the Fedora Project

## How to set up?

1. `git clone https://github.com/t0xic0der/fragment.git`
2. `cd fragment/`
3. `virtualenv venv`
4. `source venv/bin/activate`
5. `pip3 install -r requirements.txt`
6. `python3 main.py --help`
7. `python3 main.py -p 9696 -4`

## How to test changes locally using Podman?

1. Build the image `podman build . -f Dockerfile -t fedora-easyfix:latest`.
2. Start the server `podman run -p 9696:9696 -ti fedora-easyfix:latest -p 9696 -4`

Detailed documentation would arrive shortly. Inconvenience is regretted.
