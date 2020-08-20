# logboard

![develop](https://github.com/MyDataTaiwan/logboard/workflows/develop/badge.svg)

API backend for [mylog14](https://github.com/MyDataTaiwan/mylog14), an open source health record App.

# Run

1. Create a `env.sh` file wtih required environment variables:

```
#!/bin/bash

export LOG_GROUP=<AWS_LOG_GROUP>
export SECRET_KEY=<DJANGO_SECRET_KEY>
export HOST_NAMES=<HOST_NAME>
export FRONTEND_HOST_NAME=<FRONTEND_HOST_NAME>
export POSTGRES_DB=<DB_NAME>
export POSTGRESQL_DB_NAME=<DB_NAME>
export POSTGRES_USER=<DB_USER_NAME>
export POSTGRESQL_USERNAME=<DB_USER_NAME>
export POSTGRES_PASSWORD=<DB_USER_PASSWORD>
export POSTGRESQL_PASSWORD=<DB_USER_PASSWORD>
export POSTGRESQL_HOSTNAME=<DB_HOST_NAME>
export S3_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export S3_SECRET_ACCESS_KEY=<AWS_ACCESS_KEY_SECRET>
export S3_STORAGE_BUCKET_NAME=<AWS_S3_BUCKET_NAME>
```

You need to change the according settings in `logboard/settings.py` if you don't want to use specific infrastructures like AWS CloudWatch Logging or S3.

2. Install [docker compose](https://docs.docker.com/compose/) and Docker

3. Start

```
$ docker-compose up
```
