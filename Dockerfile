from python:3.7

WORKDIR /app


COPY ./requirements.txt /tmp
RUN cd /tmp && pip install -r requirements.txt
