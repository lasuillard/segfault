FROM python:3

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install libpq-dev

COPY ./django/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn==19.9.0

COPY ./django .
