FROM python:3.7-slim

ENV APP_PATH="app"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/${APP_PATH}

# Add all requirements.txt files
ADD ./requirements.txt /${APP_PATH}/requirements.txt

# Install requirements.txt
WORKDIR /${APP_PATH}

RUN /usr/local/bin/pip3 install --upgrade pip setuptools
RUN apt-get update -yqq && \
    apt-get install -yqq --force-yes --no-install-recommends default-libmysqlclient-dev && \
    apt-get install -yqq --force-yes --no-install-recommends build-essential && \
    /usr/local/bin/pip3 --no-cache-dir install -r requirements.txt && \
    apt-get purge -yqq --force-yes build-essential && \
    apt-get install -yqq --force-yes wget && \
    apt-get autoremove -yqq --force-yes

RUN wget https://github.com/schemalex/schemalex/releases/download/v0.1.1/schemalex_linux_amd64.tar.gz && \
    tar -zxvf ./schemalex_linux_amd64.tar.gz && \
    cp schemalex_linux_amd64/schemalex /usr/local/bin/schemalex && \
    chmod +x /usr/local/bin/schemalex && \
    rm -rf schemalex_linux_amd64.tar.gz && \
    rm -rf schemalex_linux_amd64 && \
    wget https://github.com/amacneil/dbmate/releases/download/v1.9.0/dbmate-linux-amd64 && \
    cp dbmate-linux-amd64 /usr/local/bin/dbmate && \
    chmod +x /usr/local/bin/dbmate && \
    rm -rf dbmate-linux-amd64

# Add python directories
# ADD . /${APP_PATH}
ADD ./deploy /${APP_PATH}/deploy
ADD ./apps /${APP_PATH}/apps
ADD ./conf /${APP_PATH}/conf
ADD ./lib /${APP_PATH}/lib
ADD ./db /${APP_PATH}/db
ADD ./manage.py /${APP_PATH}/manage.py
ADD ./api.py /${APP_PATH}/api.py

# Setup entry point
RUN mv /${APP_PATH}/deploy/entrypoint.sh /${APP_PATH}/entrypoint.sh
CMD /${APP_PATH}/entrypoint.sh
