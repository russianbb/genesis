FROM python:3.7.9-slim-buster

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    netcat \
    openssh-client

RUN apt-get clean && apt-get autoremove

EXPOSE 8080

ENV PYTHONUNBUFFERED 1

COPY /requirements/tests.txt tests.txt
RUN pip install -r tests.txt

COPY /requirements/base.txt base.txt
RUN pip install -r base.txt

COPY . /code/
WORKDIR /code/src/genesis/
