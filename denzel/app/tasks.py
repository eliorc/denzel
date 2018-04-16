import os

import celery
import requests
from app.logic import process, predict

CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

app = celery.Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


@app.task
def invoke_predict(json_data):
    # Preprocess data
    data = process(json_data)

    # Preform predictions
    result = [predict(sample) for sample in data]

    # Send prediction to callback_uri
    requests.post(url=json_data['callback_uri'],
                  json=result)

    return result
