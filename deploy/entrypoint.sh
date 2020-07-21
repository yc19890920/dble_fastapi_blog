#!/usr/bin/env bash

# set -x

source ./env


if [ "$1" == 'makemigrations' ]; then
    echo "Running $1"
    python3 manage.py makemigrations --name migrate
    exit 0
elif [ "$1" == 'migrate' ]; then
    echo "Running $1"
    python3 manage.py initdb
    python3 manage.py migrate
    exit 0
elif [ "$1" == 'createsuperuser' ]; then
    echo "Running createsuperuser"
    python3 manage.py createsuperuser
else
    exec uvicorn \
        --workers "${PYTHON_THREADS:-4}" \
        --host 0.0.0.0 \
        --port 8080 \
        --loop uvloop \
        --http httptools \
        --backlog 2048 \
        --timeout-keep-alive 300 \
        --log-level info \
        --use-colors \
        --proxy-headers \
        "api:app"
fi

