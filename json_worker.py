import json


def return_key_value_from_json(key):
    """Return value of the key from json file"""
    with open("secret.json") as json_file:
        data = json.load(json_file)
        return data[key]


def write_key_value_to_json(key, value):
    """Write key and value to json file"""
    with open("secret.json") as json_file:
        data = json.load(json_file)
        data[key] = value
    with open("secret.json", "w") as json_file:
        json.dump(data, json_file, indent=4)