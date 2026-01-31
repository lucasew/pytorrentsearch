FROM python:3.14-alpine@sha256:31da4cb527055e4e3d7e9e006dffe9329f84ebea79eaca0a1f1c27ce61e40ca5
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["pytorrentsearch"]
