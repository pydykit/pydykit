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


def transformation_matrix(quat, sign=1.0):
    tmp = np.concatenate(
        [
            -quat[1:, np.newaxis],
            quat[0] * np.eye(3) + sign * hat_map(quat=quat),
        ],
        axis=1,
    )
    assert tmp.shape == (3, 4)

    return tmp


def spatial_transformation_matrix(quat):
    return transformation_matrix(quat=quat, sign=1.0)


def convective_transformation_matrix(quat):
    return transformation_matrix(quat=quat, sign=-1.0)


def transf_matrix_sym(quat, sign=1.0):

    spatial = spatial_transformation_matrix(quat=quat)
    convective = convective_transformation_matrix(quat=quat)

    return spatial @ convective.T


def left_multiplation_matrix(quat):

    G_q = convective_transformation_matrix(quat)

    tmp = np.block([np.array([quat]).T, G_q.T])

    assert tmp.shape == (4, 4)

    return tmp


def quaternion_velocity(quaternion_position: np.array, angular_velocity: np.array):
    G_q = convective_transformation_matrix(quat=quaternion_position)
    return 0.5 * G_q.T @ angular_velocity


def discrete_gradient(
    system_n,
    system_n1,
    system_n05,
    func_name: str,
    jacobian_name: str,
    argument_n: np.ndarray,
    argument_n1: np.ndarray,
    argument_n05: np.ndarray,
    type: str = "Gonzalez",
    increment_tolerance: float = 1e-12,
):
    func_n = getattr(system_n, func_name)()
    func_n1 = getattr(system_n1, func_name)()

    if type == "Gonzalez":
        increment_norm_squared = (argument_n1 - argument_n).T @ (
            argument_n1 - argument_n
        )
        midpoint_jacobian = getattr(system_n05, jacobian_name)()
        dim_func = midpoint_jacobian.ndim
        if dim_func == 1:
            midpoint_jacobian = midpoint_jacobian[np.newaxis, :]
            func_n = np.array([func_n])
            func_n1 = np.array([func_n1])

        discrete_gradient_vector = midpoint_jacobian

        if increment_norm_squared > increment_tolerance:
            for index in range(dim_func):
                discrete_gradient_vector[index, :] += (
                    (
                        func_n1[index]
                        - func_n[index]
                        - np.dot(
                            midpoint_jacobian[index, :],
                            (argument_n1 - argument_n),
                        )
                    )
                    / increment_norm_squared
                    * (argument_n1 - argument_n)
                )
    else:
        raise NotImplementedError(type)

    return discrete_gradient_vector.squeeze()
