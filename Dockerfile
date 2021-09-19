FROM python:3.8-alpine

COPY . /opt/app

WORKDIR /opt/app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]

CMD ["-p 9696", "-4"]
