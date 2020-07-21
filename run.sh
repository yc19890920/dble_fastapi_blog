#!/usr/bin/env bash

set -x

pip="/home/microk8s/pyenv/versions/dbo_track/bin/pip"
python="/home/microk8s/pyenv/versions/dbo_track/bin/python"
uvicorn="/home/microk8s/pyenv/versions/dbo_track/bin/uvicorn"

# CREATE DATABASE IF NOT EXISTS blog DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;

#python="/home/python/pyenv/versions/3.8.2/bin/python"
#uvicorn="/home/python/pyenv/versions/3.8.2/bin/uvicorn"

# docker build -t blog:1.0 -f Dockerfile .

# docker run -it --rm blog:1.0 bash

if [ "$1" == 'makemigrations' ]; then
    echo "Running $1"
    $python manage.py makemigrations --name migrate
elif [ "$1" == 'migrate' ]; then
    echo "Running $1"
    $python manage.py initdb
    $python manage.py migrate
elif [ "$1" == 'createsuperuser' ]; then
    echo "Running createsuperuser"
    $python manage.py createsuperuser
elif [ "$1" == 'r' ]; then
    echo "Running remove __pycache__"
    find . -name '__pycache__' | xargs rm -rf {}\;
else
    exec $uvicorn \
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




