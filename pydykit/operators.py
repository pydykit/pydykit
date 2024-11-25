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
    type: str = "Gonzalez",
    increment_tolerance: float = 1e-12,
):

    if type != "Gonzalez":
        raise NotImplementedError(
            f"Discrete gradient of type {type} is not implemented."
        )

    func_n = getattr(system_n, func_name)()
    func_n1 = getattr(system_n1, func_name)()
    midpoint_jacobian = getattr(system_n05, jacobian_name)()
    midpoint_jacobian, func_n, func_n1 = adjust_midpoint_jacobian(
        midpoint_jacobian, func_n, func_n1
    )

    discrete_gradient_vector = Gonzalez_discrete_gradient(
        func_n,
        func_n1,
        midpoint_jacobian,
        argument_n,
        argument_n1,
        increment_tolerance,
    )

    return discrete_gradient_vector.squeeze()


def Gonzalez_discrete_gradient(
    func_n,
    func_n1,
    midpoint_jacobian,
    argument_n,
    argument_n1,
    denominator_tolerance,
):
    """Compute the discrete gradient using the Gonzalez approach."""
    discrete_gradient = midpoint_jacobian.copy()
    increment = argument_n1 - argument_n
    denominator = increment.T @ increment

    if denominator > denominator_tolerance:

        for index in range(midpoint_jacobian.shape[0]):
            discrete_gradient[index, :] += (
                (
                    func_n1[index]
                    - func_n[index]
                    - np.dot(midpoint_jacobian[index, :], increment)
                )
                / denominator
                * increment.T
            )

        return discrete_gradient

    else:
        return midpoint_jacobian


def adjust_midpoint_jacobian(midpoint_jacobian, func_n, func_n1):
    """Helper function to adjust the midpoint Jacobian and function evaluations for scalar-valued functions."""
    if midpoint_jacobian.ndim == 1:
        return midpoint_jacobian[np.newaxis, :], np.array([func_n]), np.array([func_n1])
    return midpoint_jacobian, func_n, func_n1
