#!/bin/bash

PROJECT_NAME=$1

if [ -f .building ]; then
    touch .api_pip
    pip install --upgrade -r requirements.txt
    rm .api_pip
fi

rm -f .building
gunicorn -b 0.0.0.0:8000 app:app

