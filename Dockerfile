FROM registry.fedoraproject.org/fedora-minimal:35
RUN microdnf install -y \
      python3-pip \
      util-linux \
      tar \
      gzip \
      python3 \
      python3-flask \
      python3-requests \
      python3-gevent \
      python3-beautifulsoup4 \
      python3-flask-socketio \
      python3-flask-caching \
      python3-rq \
      python3-redis \
      python3-gunicorn \
      python3-dateutil \
      fedora-messaging \
    && microdnf clean all
WORKDIR /opt/app
# need to package this one
RUN pip3 install gevent-websocket
COPY mote mote
COPY fedora-messaging.toml /etc/fedora-messaging/config.toml
RUN sed -i "s/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/$(uuidgen)/g" \
    /etc/fedora-messaging/config.toml
EXPOSE 9696/tcp
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:9696", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w1", "mote.main:main"]


