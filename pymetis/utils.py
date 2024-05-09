import numpy as np
import yaml


def load_yaml_file(path):
    with open(path, "r") as file:
        content = yaml.safe_load(file)
    return content


class PymetisException(Exception):
    pass


def get_numerical_tangent(func, state_1, state_2, epsilon=1e-10):

    state_1 = state_1.copy()
    state_2 = state_2.copy()

    N = len(state_2)
    tang_num = np.zeros((N, N))

    for j in range(N):

        xsave = state_2[j]

        delp = epsilon * (1.0 + abs(xsave))
        state_2[j] = xsave + delp

        R1 = func(
            state_n=state_1,
            state_n1=state_2,
        )

        state_2[j] = xsave - delp

        R2 = func(
            state_n=state_1,
            state_n1=state_2,
        )

        state_2[j] = xsave

        tang_num[:, j] = (R1 - R2) / (2.0 * delp)

    return tang_num
