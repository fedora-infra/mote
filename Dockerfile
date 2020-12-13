FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /mote
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN sed -i 's|json_cache_location = "/var/cache/httpd/mote/cache.json"|json_cache_location = "./cache.json"|' ./mote/config.py
COPY . .
EXPOSE 5000
CMD ["python3", "runmote.py"]