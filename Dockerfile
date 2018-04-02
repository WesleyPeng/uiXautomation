FROM python:latest

COPY src /usr/local/src
COPY build.py /usr/local
COPY build.sh /usr/local
WORKDIR /usr/local

ENTRYPOINT ["./build.sh"]
