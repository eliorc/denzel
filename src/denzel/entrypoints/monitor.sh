#!/bin/bash

PROJECT_NAME=$1

if [ -f .building ]; then
    touch .monitor_pip
    pip install --upgrade -r requirements.txt
    rm .monitor_pip
fi

rm -f .building
flower -A app.tasks --port=5555 --broker=redis://redis:6379/0

