Denzel Deployment Framework
===========================

.. figure:: _static/logo_icon.svg
    :width: 10%
    :align: center


| `Denzel`_ is a model-agnostic lean framework for fast and easy API deployment of machine learning models.
| Denzel is data scientist first; while it leverages production grade tools and practices, its main goal is to abstract the mechanics from the data scientist allowing model deployment with ease.

.. warning::

    Denzel only works on Linux environment at the moment.

.. _`Denzel`: https://github.com/eliorc/denzel

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   intro
   tutorial
   pipeline
   endpoints
   cli

Showcase
--------

| Deployment with denzel is very simple.
| Assuming we have saved to disk an already trained model with less than 60 lines you can have it deployed with the following features:
| 1. Expose an API for users to use your model
| 2. Allow users to check their prediction request status through API requests
| 3. Monitor the performance of your deployment through `Flower UI`_
| 4. Fully containerized system so it could be deployed anywhere
|
| Here is an example of all the code necessary to deploy the Iris classifier from the :doc:`tutorial <tutorial>`.

.. code-block:: python3

   import pickle
   import numpy as np

   FEATURES = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width']

   # -------- Handled by api container --------
   def verify_input(json_data):
       """ Verifies the validity of an API request content """

       # callback_uri is needed to sent the responses to - NOT NEEDED WHEN USING SYNCHRONOUS RESPONSES
       if 'callback_uri' not in json_data:
           raise ValueError('callback_uri not supplied')

       # Verify data was sent
       if 'data' not in json_data:
           raise ValueError('no data to predict for!')

       # Verify data structure
       if not isinstance(json_data['data'], dict):
           raise ValueError('json_data["data"] must be a mapping between unique id and features')

       # Verify data scheme
       for unique_id, features in json_data['data'].items():
           feature_names = features.keys()
           feature_values = features.values()

           # Verify all features needed were sent
           if not all([feature in feature_names for feature in FEATURES]):
               raise ValueError('For each example all of the features [{}] must be present'.format(FEATURES))

           # Verify all features that were sent are floats
           if not all([isinstance(value, float) for value in feature_values]):
               raise ValueError('All feature values must be floats')

       return json_data


   # -------- Handled by denzel container --------
   def load_model():
       """ Load model and its assets to memory """
       with open('./app/assets/iris_svc.pkl', 'rb') as model_file:
           loaded_model = pickle.load(model_file)

       return loaded_model


   def process(model, json_data):
       """ Process the json_data passed from verify_input to model ready data """

       # Gather unique IDs
       ids = json_data['data'].keys()

       # Gather feature values and make sure they are in the right order
       data = []
       for features in json_data['data'].values():
           data.append([features[FEATURES[0]], features[FEATURES[1]], features[FEATURES[2]], features[FEATURES[3]]])

       data = np.array(data)

       return ids, data


   def predict(model, data):
       """ Predicts and prepares the answer for the API-caller """

       # Unpack the outputs of process function
       ids, data = data

       # Predict
       predictions = model.predict(data)

       # Pack the IDs supplied by the end user and their corresponding predictions in a dictionary
       response = dict(zip(ids, predictions))

       return response

.. _`Flower UI`: https://flower.readthedocs.io/en/latest/screenshots.html
.. _`development_state`:

Development State
-----------------

| Denzel is supported by `Data Science Group Ltd.`_ and is promised to be kept on open source.
| Denzel right now is on alpha. This means that it is fully operational and new features and support will be added to it before moving on to a beta release.

.. _`Data Science Group Ltd.`: http://www.datascience.co.il/
