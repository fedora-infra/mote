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
3. To start the server on a non default port: `docker run <docker host port>:<container port> <hash of image> -p <container port> -4`

Detailed documentation would arrive shortly. Inconvenience is regretted.
