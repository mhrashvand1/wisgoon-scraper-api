# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

WORKDIR /usr/src/app/api

CMD while ! python manage.py test_celery_broker > /dev/null 2>&1; do sleep 1; done && \
    mkdir -p /var/run/celery/ && mkdir -p /var/log/celery/ && \
    celery -A config multi start run_crawler_worker -Q run_crawler_queue -l info -E --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log && \
    while ! python manage.py sqlflush > /dev/null 2>&1; do sleep 1; done && \
    python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \ 
    while python manage.py createsuperuser --noinput; do sleep 0.1; done && \
    gunicorn -b 0.0.0.0:8000 config.wsgi;

