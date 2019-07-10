#!/bin/bash

PROJECT_NAME=$1

if [[ -f .building ]] || [[ -f .updatepipreqs ]]; then
    touch .api_pip
    pip install --upgrade -r requirements.txt
    rm .api_pip
fi

if [[ -f .building ]] || [[ -f .updateosreqs ]]; then
    touch .api_os
    /bin/bash requirements.sh
    rm .api_os
fi

rm -f .building
gunicorn -b 0.0.0.0:8000 app:app
