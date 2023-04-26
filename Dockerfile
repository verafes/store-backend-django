# base image
FROM python:3.11-slim-buster

# creating directory for app and cd into it
WORKDIR /app

# copying from local disk to container
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
# RUN python manage.pt collectstatic --noinput

# running server
EXPOSE 8080
CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8080']
#CMD {".bin/bash"}
