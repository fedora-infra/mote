FROM python:3.8-alpine

COPY . /opt/app

WORKDIR /opt/app

COPY . /opt/app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "./main.py"]

CMD ["-p 9696", "-4"]