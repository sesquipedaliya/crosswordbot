FROM python:3.7-alpine
COPY requirements.txt /
RUN set -fue; \
	apk add --virtual build-deps file make gcc musl-dev libffi-dev; \
	pip install -r /requirements.txt; \
	apk del build-deps file make gcc musl-dev libffi-dev; \
	rm -r /root/.cache
COPY *.py /app/
WORKDIR /app
CMD ["python", "-u", "main.py"]
