FROM python:3.6-alpine

WORKDIR /app

COPY enaFastqFetch.py /app

RUN pip install --no-cache-dir requests

ENTRYPOINT ["python", "enaFastqFetch.py"]
