FROM python:3.8

WORKDIR /opt/app

COPY . /opt/app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "./main.py"]

CMD ["-p 3696", "-4"]