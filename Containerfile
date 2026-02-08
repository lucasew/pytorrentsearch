FROM python:3.13-alpine@sha256:bb1f2fdb1065c85468775c9d680dcd344f6442a2d1181ef7916b60a623f11d40
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["pytorrentsearch"]
