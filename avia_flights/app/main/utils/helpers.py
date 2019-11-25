import os


def convert_to_dict(data: list) -> dict:
    json_data = {}
    for i, el in enumerate(data):
        json_data[i] = el.to_dict()
    return json_data


def listdir_full_path(path: str) -> list:
    return [os.path.join(path, f) for f in os.listdir(path)]
