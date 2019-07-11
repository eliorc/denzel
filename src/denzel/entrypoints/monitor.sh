#!/bin/bash

PROJECT_NAME=$1

if [[ -f .building ]] || [[ -f .updatepipreqs ]]; then
    touch .monitor_pip
    pip install --upgrade -r requirements.txt
    rm .monitor_pip
fi

if [[ -f .building ]] || [[ -f .updateosreqs ]]; then
    touch .monitor_os
    /bin/bash requirements.sh
    rm .monitor_os
fi

rm -f .building
flower -A app.tasks --port=5555 --broker=redis://redis:6379/0
