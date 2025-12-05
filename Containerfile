FROM python:3.13-alpine@sha256:65fe04ddc51a8ccbf14ecb882903251e4a124914673001b03c393eb65dd9502a
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["pytorrentsearch"]
