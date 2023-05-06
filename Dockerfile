FROM python:3.6-slim-buster
RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install gunicorn
RUN mkdir /var/log/fetlla
RUN apt-get update -y  && apt install build-essential -y
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . ./app
WORKDIR /app
EXPOSE 8000
ENTRYPOINT sh entrypoint.sh