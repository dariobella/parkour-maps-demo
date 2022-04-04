FROM python:3.10.3-alpine3.15

WORKDIR /backend

COPY requirements.txt requirements.txt

RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base
RUN apk add netcat-openbsd

RUN pip install -r ./requirements.txt