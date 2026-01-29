FROM python:3.13-alpine@sha256:9298134acf0820ed89d8259944248b24b41e4de911a083f33bd70b583acc368a
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["pytorrentsearch"]
