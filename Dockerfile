FROM python:3.8-slim
WORKDIR /mote
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN sed -i 's|json_cache_location = "/var/cache/httpd/mote/cache.json"|json_cache_location = "./cache.json"|' ./mote/config.py
EXPOSE 5000
COPY . .
CMD ["python3", "runmote.py"]
