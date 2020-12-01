FROM python:3.9-alpine
MAINTAINER Goeun1001

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add mysql mysql-client mysql-dev
RUN apk update && apk add gcc libc-dev make git \
    libffi-dev openssl-dev python3-dev libxslt-dev
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
