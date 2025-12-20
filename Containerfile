FROM python:3.13-alpine@sha256:e7e041128ffc3e3600509f508e44d34ab08ff432bdb62ec508d01dfc5ca459f7
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["pytorrentsearch"]
