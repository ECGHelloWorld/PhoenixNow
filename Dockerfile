FROM alpine:latest

RUN apk add --no-cache python3-dev openssl-dev libressl-dev libffi-dev musl-dev gcc && pip3 install --upgrade pip


WORKDIR /app

COPY . /app

RUN pip3 --no-cache install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "server.py" ]