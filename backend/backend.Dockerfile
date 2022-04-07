FROM python:3.9.12-slim-buster

WORKDIR /backend

COPY requirements.txt requirements.txt

RUN apt-get update && apt install -y netcat && apt-get install -y default-libmysqlclient-dev build-essential && apt-get install -y default-libmysqlclient-dev && apt-get install -y python-mysqldb

RUN pip install -r ./requirements.txt