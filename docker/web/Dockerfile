# pull official base image
FROM python:3.8-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache \
        postgresql-dev \
        musl-dev \
        gcc \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
        gettext-dev \
        # Required for installing/upgrading Pillow
        jpeg-dev zlib-dev libjpeg \
    && apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        libcrypto1.1 \
    && apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        gdal-dev \
        geos-dev \
        proj-dev

# Add postgis extension
COPY ./docker/db/db.sql /docker-entrypoint-initdb.d/

# set work directory
RUN mkdir /code
WORKDIR /code

# install dependencies
RUN pip install --upgrade pipenv
COPY ./Pipfile .
# COPY ./Pipfile.lock .
RUN pipenv install --dev --deploy

# copy project
COPY . /code/