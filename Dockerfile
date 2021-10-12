FROM python:3.8-alpine
COPY . /opt/app
LABEL maintainer "Anurag Phadnis <phadnis.anurag@gmail.com>"
WORKDIR /opt/app
RUN pip3 install -r requirements.txt
RUN python setup.py install
EXPOSE 9696/tcp
ENTRYPOINT ["start-mote-server"]
CMD ["-p 9696", "-4"]
