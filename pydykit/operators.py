import numpy as np


def get_skew_matrix(vector):

    assert len(vector) == 4, "Expect vector to be of length four"

    return np.array(
        [
            [0.0, -vector[3], vector[2]],
            [vector[3], 0.0, -vector[1]],
            [-vector[2], vector[1], 0.0],
        ]
    )


def get_transf_matrix(vector, sign=1.0):
    tmp = np.concatenate(
        [
            -vector[1:, np.newaxis],
            vector[0] * np.eye(3) + sign * get_skew_matrix(vector=vector),
        ],
        axis=1,
    )
    assert tmp.shape == (3, 4)

    return tmp


def get_transf_matrix_sym(vector, sign=1.0):

    positive = get_transf_matrix(vector=vector, sign=1.0)
    negative = get_transf_matrix(vector=vector, sign=-1.0)

    return positive @ negative.T
