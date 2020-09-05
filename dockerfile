FROM python:3.7.3
ENV PYTHONUNBUFFERED 1

ADD /requirements/base.txt base.txt
ADD /requirements/tests.txt tests.txt

RUN pip install -r base.txt
RUN pip install -r tests.txt

COPY . /code/
WORKDIR /code/

WORKDIR /code/src/genesis/
