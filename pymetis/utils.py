import numpy as np
import yaml


def load_yaml_file(path):
    with open(path, "r") as file:
        content = yaml.safe_load(file)
    return content


class PymetisException(Exception):
    pass


class States:
    def __init__(self, nbr_states, dim_state):
        self.state = np.zeros((nbr_states, dim_state))
        self.state_n = np.zeros(dim_state)
        self.state_n1 = np.zeros(dim_state)

        self.time = np.zeros(nbr_states)
