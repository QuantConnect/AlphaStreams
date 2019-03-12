import json


def test_config():
    config_path = "config.json"

    with open(config_path) as f:
        config = json.load(f)

    return config


def read_test_data(file_name):
    with open("TestData/" + file_name, "r") as f:
        text = f.read()
        text = text.strip("\n")
        return text.split("\n")


def get_string_list(list_objects):
    result = []
    for obj in list_objects:
        result.append(str(obj))
    return result


def save_test_data(file_name, list_objects):
    with open("TestData/" + file_name, "w") as f:
        for obj in list_objects:
            f.write(str(obj) + "\n")
    return
