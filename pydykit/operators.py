import numpy as np


def decompose_quaternion(quaternion):
    scalar = quaternion[0]
    vector = quaternion[1:]
    return scalar, vector


def hat_map(quat):

    assert len(quat) == 4, "Expect vector to be of length four"

    return np.array(
        [
            [0.0, -quat[3], quat[2]],
            [quat[3], 0.0, -quat[1]],
            [-quat[2], quat[1], 0.0],
        ]
    )


def get_transformation_matrix(quat, sign=1.0):
    tmp = np.concatenate(
        [
            -quat[1:, np.newaxis],
            quat[0] * np.eye(3) + sign * hat_map(quat=quat),
        ],
        axis=1,
    )
    assert tmp.shape == (3, 4)

    return tmp


def get_spatial_transformation_matrix(quat):
    return get_transformation_matrix(quat=quat, sign=1.0)


def get_convective_transformation_matrix(quat):
    return get_transformation_matrix(quat=quat, sign=-1.0)


def get_transf_matrix_sym(quat, sign=1.0):

    spatial = get_spatial_transformation_matrix(quat=quat)
    convective = get_convective_transformation_matrix(quat=quat)

    return spatial @ convective.T


def get_left_multiplation_matrix(quat):

    G_q = get_convective_transformation_matrix(quat)

    tmp = np.block([np.array([quat]).T, G_q.T])

    assert tmp.shape == (4, 4)

    return tmp
