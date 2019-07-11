#!/bin/bash

PROJECT_NAME=$1

if [[ -f .building ]] || [[ -f .updatepipreqs ]]; then
    touch .denzel_pip
    pip install --upgrade -r requirements.txt
    rm .denzel_pip
fi

if [[ -f .building ]] || [[ -f .updateosreqs ]]; then
    touch .denzel_os
    /bin/bash requirements.sh
    rm .denzel_os
fi

rm -f .building
celery -A app.tasks worker --loglevel=info --logfile=logs/worker.log -n worker@$PROJECT_NAME
