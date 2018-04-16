def verify_input(json_data):
    # TODO - DSG - verify the input data format
    if 'callback_uri' not in json_data:
        raise ValueError('callback_uri not supplied')

    return json_data


def process(json_data):
    # TODO - DSG - transform data into model ready data. Must return list, where each element is an example.
    return []


def predict(data):
    # TODO - DSG - Perform prediction. Must return dictionary of {<id>: <result>}
    return {'id': 42, 'id2': 42}
