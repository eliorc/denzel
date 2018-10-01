#!/bin/bash

PROJECT_NAME=$1

if [ -f .building ]; then
    touch .denzel_pip
    pip install --upgrade -r requirements.txt
    rm .denzel_pip
fi

rm -f .building
celery -A app.tasks worker --loglevel=info --logfile=logs/worker.log -n worker@$PROJECT_NAME

