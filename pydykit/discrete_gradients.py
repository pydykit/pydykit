import numpy as np

from . import abstract_base_classes


class GonzalezDiscreteGradient(abstract_base_classes.DiscreteGradient):
    def compute(
        self,
        system_n,
        system_n1,
        system_n05,
        func_name: str,
        jacobian_name: str,
        argument_n: np.ndarray,
        argument_n1: np.ndarray,
        increment_tolerance: float = 1e-12,
        **kwargs,
    ) -> np.ndarray:
        func_n = getattr(system_n, func_name)()
        func_n1 = getattr(system_n1, func_name)()
        midpoint_jacobian = getattr(system_n05, jacobian_name)()
        midpoint_jacobian, func_n, func_n1 = adjust_midpoint_jacobian(
            midpoint_jacobian, func_n, func_n1
        )

        return Gonzalez_discrete_gradient(
            func_n,
            func_n1,
            midpoint_jacobian,
            argument_n,
            argument_n1,
            increment_tolerance,
        )


class GonzalezDecomposedDiscreteGradient(abstract_base_classes.DiscreteGradient):
    def compute(
        self,
        system_n,
        system_n1,
        system_n05,
        func_name: str,
        jacobian_name: str,
        argument_n: np.ndarray,
        argument_n1: np.ndarray,
        nbr_func_parts: int,
        func_parts_n,
        func_parts_n1,
        increment_tolerance: float = 1e-12,
        **kwargs,
    ) -> np.ndarray:
        discrete_gradient = []

        for index in range(nbr_func_parts):
            func_n = getattr(system_n, f"{func_name}_{index+1}")()
            func_n1 = getattr(system_n1, f"{func_name}_{index+1}")()
            midpoint_jacobian = getattr(system_n05, f"{jacobian_name}_{index+1}")()
            midpoint_jacobian, func_n, func_n1 = adjust_midpoint_jacobian(
                midpoint_jacobian, func_n, func_n1
            )

            part_argument_n = system_n.decompose_state()[func_parts_n[index]]
            part_argument_n1 = system_n1.decompose_state()[func_parts_n1[index]]

            contribution = Gonzalez_discrete_gradient(
                func_n,
                func_n1,
                midpoint_jacobian,
                part_argument_n,
                part_argument_n1,
                increment_tolerance,
            )

            discrete_gradient.append(contribution.squeeze())

        return np.concatenate(discrete_gradient, axis=0)


class DiscreteGradientFactory:
    """Factory for creating discrete gradient instances."""

    @staticmethod
    def create(type: str) -> abstract_base_classes.DiscreteGradient:
        if type == "Gonzalez":
            return GonzalezDiscreteGradient()
        elif type == "Gonzalez_decomposed":
            return GonzalezDecomposedDiscreteGradient()
        else:
            raise ValueError(f"Unsupported discrete gradient type: {type}")


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
    **kwargs,
):
    gradient_computer = DiscreteGradientFactory.create(type)

    return gradient_computer.compute(
        system_n=system_n,
        system_n1=system_n1,
        system_n05=system_n05,
        func_name=func_name,
        jacobian_name=jacobian_name,
        argument_n=argument_n,
        argument_n1=argument_n1,
        increment_tolerance=increment_tolerance,
        **kwargs,
    )


def Gonzalez_discrete_gradient(
    func_n,
    func_n1,
    midpoint_jacobian,
    argument_n,
    argument_n1,
    denominator_tolerance,
):
    """Compute the discrete gradient using the Gonzalez approach."""
    discrete_gradient = midpoint_jacobian
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

        result = discrete_gradient

    else:
        result = midpoint_jacobian

    return result.squeeze()


def adjust_midpoint_jacobian(midpoint_jacobian, func_n, func_n1):
    """Helper function to adjust the midpoint Jacobian and function evaluations for scalar-valued functions."""
    if midpoint_jacobian.ndim == 1:
        return midpoint_jacobian[np.newaxis, :], np.array([func_n]), np.array([func_n1])
    return midpoint_jacobian, func_n, func_n1
