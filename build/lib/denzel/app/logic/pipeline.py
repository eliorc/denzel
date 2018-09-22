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

    return json_data


# -------- Handled by denzel container --------
def load_model():
    """
    Load model and its assets to memory

    :return: Model, will be used by the predict and process functions
    """

    return  # return the loaded model object


def process(model, json_data):
    """
    Process the json_data passed from verify_input to model ready data

    :param model: Loaded object from load_model function
    :param json_data: Data from the verify_input function
    :return: Model ready data
    """

    # return model ready data
    return


def predict(model, data):
    """
    Predicts and prepares the answer for the API-caller

    :param model: Loaded object from load_model function
    :param data: Data from process function
    :return: Response to API-caller
    :rtype: dict
    """

    # return a dictionary that will be parsed to JSON and sent back to API-caller
    return {}
