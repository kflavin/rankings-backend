FROM alpine:3.7
MAINTAINER Kyle Flavin
# docker run -it -e DATABASE_URL=postgresql://<user>@docker.for.mac.localhost:5432/table -p 5000:8000 rankings-backend:latest

RUN apk update && \
    apk add python3 py3-psycopg2 gcc python3-dev musl-dev libffi-dev && \
    easy_install-3.6 pip
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["/usr/bin/gunicorn", "manage:app", "-b", "0.0.0.0"]
