FROM ubuntu:latest
LABEL authors="sinas"

ENTRYPOINT ["top", "-b"]