FROM python:3-alpine

# Install dependencies required for psycopg2 python package
RUN apk update && apk add libpq jpeg-dev zlib-dev
RUN apk update && apk add --virtual .build-deps gcc g++ python3-dev musl-dev postgresql-dev libffi-dev

RUN mkdir -p /usr/src/logboard
WORKDIR /usr/src/logboard
COPY . .
RUN mv wait-for /bin/wait-for

RUN pip install --no-cache-dir -r requirements.txt

# Remove dependencies only required for psycopg2 build
RUN apk del .build-deps

EXPOSE 8000

CMD ["gunicorn", "logboard.wsgi", "0:8000", "--log-level=info", "--access-logfile", "-", "--enable-stdio-inheritance", "--workers", "4"]
