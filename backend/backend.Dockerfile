FROM python:3.8.13-slim-buster

WORKDIR /backend

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y netcat && apt-get -y install gcc && apt-get install -y default-libmysqlclient-dev

RUN pip install -r ./requirements.txt