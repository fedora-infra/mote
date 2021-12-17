FROM registry.fedoraproject.org/fedora-minimal
RUN microdnf install -y python util-linux && microdnf clean all
ADD https://github.com/fedora-infra/fedora-messaging/raw/stable/configs/cacert.pem /etc/fedora-messaging/
ADD https://github.com/fedora-infra/fedora-messaging/raw/stable/configs/fedora-cert.pem /etc/fedora-messaging/
ADD https://github.com/fedora-infra/fedora-messaging/raw/stable/configs/fedora-key.pem /etc/fedora-messaging/
WORKDIR /opt/app
COPY requirements.txt /opt/app
RUN pip3 install -r requirements.txt
COPY src /opt/app
COPY fedora-messaging.toml /etc/fedora-messaging/config.toml
RUN sed -ie "s/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/$(uuidgen)/g" \
    /etc/fedora-messaging/config.toml
EXPOSE 9696/tcp
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:9696", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w1", "mote.main:main"]
