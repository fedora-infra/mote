FROM registry.fedoraproject.org/fedora-minimal:38 as base
FROM base as builder
RUN microdnf install -y python3-pip && microdnf clean all
WORKDIR /tmp
RUN pip3 install --disable-pip-version-check poetry
COPY poetry.lock pyproject.toml .
RUN poetry export --without-hashes --no-interaction --no-ansi -o requirements.txt

FROM base as runtime
RUN microdnf update -y && microdnf install -y python3-pip util-linux tar gzip && microdnf clean all
ADD https://github.com/fedora-infra/fedora-messaging/raw/stable/configs/cacert.pem /etc/fedora-messaging/
ADD https://github.com/fedora-infra/fedora-messaging/raw/stable/configs/fedora-cert.pem /etc/fedora-messaging/
ADD https://github.com/fedora-infra/fedora-messaging/raw/stable/configs/fedora-key.pem /etc/fedora-messaging/
RUN chmod 640 /etc/fedora-messaging/*.pem
WORKDIR /opt/app
COPY --from=builder /tmp/requirements.txt .
RUN pip3 install -r requirements.txt
COPY mote mote
COPY fedora-messaging.toml /etc/fedora-messaging/config.toml
RUN sed -i "s/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/$(uuidgen)/g" \
    /etc/fedora-messaging/config.toml
EXPOSE 9696/tcp
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:9696", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w1", "mote.main:main"]
