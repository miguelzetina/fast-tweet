FROM python:3.10-alpine3.14

ENV SITE_DIR /usr/src
RUN mkdir -p $SITE_DIR
WORKDIR $SITE_DIR
ENV PYTHONUNBUFFERED 1

RUN apk add postgresql-dev \
            gcc \
            musl-dev \
            g++

COPY . /usr/src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt