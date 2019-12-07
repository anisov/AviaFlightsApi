import os


def convert_to_dict(lst: list) -> dict:
    data = {}
    for i, el in enumerate(lst):
        data[i] = el.to_dict()
    return data


def listdir_full_path(path: str) -> list:
    return [os.path.join(path, f) for f in os.listdir(path)]
