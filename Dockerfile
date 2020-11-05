FROM python:3.8-slim
WORKDIR /mote
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "runmote.py"]
