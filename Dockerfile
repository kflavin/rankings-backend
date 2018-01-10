FROM alpine:3.7
MAINTAINER Kyle Flavin

RUN apk update && \
    apk add python3 py3-psycopg2 gcc python3-dev musl-dev libffi-dev && \
    easy_install-3.6 pip
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["/usr/bin/gunicorn", "manage:app"]
