FROM python:3.13-alpine@sha256:2f607129b1b915a949320bf0c4831a73d1c1b1be663c2b1d8c93aa35a5f44a95
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["pytorrentsearch"]
