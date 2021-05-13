FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /mote
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000