ARG PYTHON_VERSION=3.6-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

#install the linux packages, since these are the dependencies of some python packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    cron \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/* !

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code


CMD ["gunicorn", "--workers", "2", "backend.wsgi"]





# FROM python:3.6-slim-buster
# RUN pip install --upgrade pip
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# RUN pip install gunicorn
# RUN mkdir /var/log/fetlla
# RUN apt-get update -y  && apt install build-essential -y
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt
# COPY . ./app
# WORKDIR /app
# EXPOSE 8000
# ENTRYPOINT sh entrypoint.sh