import ujson

import falcon
from celery.result import AsyncResult
from app.tasks import invoke_predict
from app.logic.pipeline import verify_input


INFO_FILE = './app/assets/info.txt'


class InfoResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""

        resp.status = falcon.HTTP_200

        with open(INFO_FILE) as info_file:
            info = ''.join(info_file)

        resp.body = info


class StatusResource(object):

    def on_get(self, req, resp, task_id):
        """Handles GET requests"""

        task_result = AsyncResult(task_id)
        result = {'status': task_result.status, 'result': task_result.result}
        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps(result)


class PredictResource(object):

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


# Never change this.
app = falcon.API()

# Create resources
info = InfoResource()
predict = PredictResource()
status = StatusResource()

# Routing
app.add_route('/info', info)
app.add_route('/predict', predict)
app.add_route('/status/{task_id}', status)
