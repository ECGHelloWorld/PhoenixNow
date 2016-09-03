FROM python:3.5-alpine
MAINTAINER Nicholas Day <nick@nickendo.com>

RUN apk update && apk add build-base mariadb-dev libffi-dev python3-dev build-base linux-headers pcre-dev

ENV INSTALL_PATH /phoenixnow
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3031

CMD uwsgi --socket :3031 -w run:app
