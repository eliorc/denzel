import pickle
import numpy as np

FEATURES = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width']

# -------- Handled by api container --------
def verify_input(json_data):
    """
    Verifies the validity of an API request content

    :param json_data: Parsed JSON accepted from API call
    :type json_data: dict
    :return: Data for the the process function
    """

    # callback_uri is needed to sent the responses to
    if 'callback_uri' not in json_data:
        raise ValueError('callback_uri not supplied')

    # Verify data was sent
    if 'data' not in json_data:
        raise ValueError('no data to predict for!')

    # Verify data structure
    if not isinstance(json_data['data'], dict):
        raise ValueError('jsondata["data"] must be a mapping between unique id and features')

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
    """
    Load model and its assets to memory
    :return: Model, will be used by the predict and process functions
    """
    with open('./app/assets/iris_svc.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    return loaded_model


def process(model, json_data):
    """
    Process the json_data passed from verify_input to model ready data

    :param model: Loaded object from load_model function
    :param json_data: Data from the verify_input function
    :return: Model ready data
    """

    # Gather unique IDs
    ids = json_data['data'].keys()

    # Gather feature values and make sure they are in the right order
    data = []
    for features in json_data['data'].values():
        data.append([features[FEATURES[0]], features[FEATURES[1]], features[FEATURES[2]], features[FEATURES[3]]])

    data = np.array(data)
    """
    data = [[float, float, float, float],
            [float, float, float, float]]
    """

    return ids, data


def predict(model, data):
    """
    Predicts and prepares the answer for the API-caller

    :param model: Loaded object from load_model function
    :param data: Data from process function
    :return: Response to API-caller
    :rtype: dict
    """

    # Unpack the outputs of process function
    ids, data = data

    # Predict
    predictions = model.predict(data)

    # Pack the IDs supplied by the end user and their corresponding predictions in a dictionary
    response = dict(zip(ids, predictions))

    return response
