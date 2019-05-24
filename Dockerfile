FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /app
RUN mkdir src

ADD requirements.txt /app

RUN apt-get update 
RUN apt-get install build-essential curl -y
RUN pip3 install -r requirements.txt
RUN apt-get --purge autoremove build-essential -y

COPY src/ /app/src/

EXPOSE ${PORT}