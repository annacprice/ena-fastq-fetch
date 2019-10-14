FROM python:3.6-alpine

WORKDIR /data

COPY enaFastqFetch /usr/local/bin

RUN pip install --upgrade pip && \ 
pip install --no-cache-dir requests

ENV PATH="/usr/local/bin:${PATH}"

ENTRYPOINT ["enaFastqFetch"]
