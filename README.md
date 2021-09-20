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

## How to run using docker

1. Build the docker image `docker build -t <tag> .`
2. Start the server `docker run -p <docker host port>:9696 <hash of image>`

Detailed documentation would arrive shortly. Inconvenience is regretted.
