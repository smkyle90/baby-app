# pull official base image
FROM python:3.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat
RUN apt-get install -y python3-dev libpq-dev
RUN apt-get install -y libxml2-dev libxslt-dev cython3

RUN apt-get install -y python-psycopg2
RUN apt-get install -y python3-lxml zlib1g-dev


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
