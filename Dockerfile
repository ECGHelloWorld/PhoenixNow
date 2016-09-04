FROM python:3.5-alpine
MAINTAINER Nicholas Day <nick@nickendo.com>

RUN apk update && apk add build-base mariadb-dev libffi-dev python3-dev build-base linux-headers pcre-dev wget

ENV DOCKERIZE_VERSION v0.2.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz 

ENV INSTALL_PATH /phoenixnow
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3031

CMD dockerize -wait tcp://db:3306 && uwsgi --socket :3031 -w run:app