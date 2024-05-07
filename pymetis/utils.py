import numpy as np
import yaml


def load_yaml_file(path):
    with open(path, "r") as file:
        content = yaml.safe_load(file)
    return content


class PymetisException(Exception):
    pass
