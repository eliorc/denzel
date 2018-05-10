import ujson

import falcon
from celery.result import AsyncResult
from app.tasks import invoke_predict
from app.logic import verify_input, process

# TODO - Fill in "Usage" section in app/info.txt
# TODO - Support for batching
# TODO - Support for partially bad input json. Now if one field is missing in one example, nothing will be predicted.

INFO_FILE = './app/info.txt'

class InfoResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        with open(INFO_FILE) as info_file:
            info = ''.join(info_file)

        resp.body = info


class StatusResource(object):

    def on_get(self, req, resp, task_id):
        task_result = AsyncResult(task_id)
        result = {'status': task_result.status, 'result': task_result.result}
        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps(result)


class PredictResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        # TODO: DSG - Rewrite this to describe what is the expected input and output of the API
        resp.body = ('This is the PREDICT endoint. \n'
                     'Both requests and responses are served in JSON. \n'
                     '\n\n'
                     'INPUT: \n'
                     '   "callback_uri": [string]           \n'     # String
                     '   "data": {                          \n'     # Dictionary
                     '      {"id": {                        \n'     # Dictionary            
                     '          "sepal_length": [float],    \n'     # Feature
                     '          "sepal_width": [float],     \n'     # Feature
                     '          "petal_length": [float],    \n'     # Feature
                     '          "petal_width": [float]      \n\n'   # Feature
                     'OUTPUT: Prediction (Species)          \n'
                     '   "Species": [string]                \n\n')  # String

    def on_post(self, req, resp):
        """Handles POST requests"""

        # Read request
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Stream read error',
                                   str(ex))

        # Parse to json
        try:
            json_data = ujson.loads(raw_json.decode())
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body.')

        # Verify json fields
        try:
            json_data = verify_input(json_data)
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Bad input format',
                                   str(ex))

        try:
            resp.status = falcon.HTTP_200
            task = invoke_predict.delay(json_data)
            resp.body = ujson.dumps({
                'status': 'success',
                'data': {
                    'task_id': task.id
                }})
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Error invoking predict',
                                   str(ex))


# falcon.API instances are callable WSGI apps. Never change this.
app = falcon.API()

# Resources are represented by long-lived class instances. Each Python class becomes a different "URL directory"
info = InfoResource()
predict = PredictResource()
status = StatusResource()

# Routing
app.add_route('/info', info)
app.add_route('/predict', predict)
app.add_route('/status/{task_id}', status)

