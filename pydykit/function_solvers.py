import abc
from typing import Callable

import numpy as np
import numpy.typing as npt
from scipy.optimize import root

from . import utils


class FunctionSolver(abc.ABC):

    @abc.abstractmethod
    def solve(
        self,
        func: Callable,
        jacobian: Callable,
        initial: npt.ArrayLike,
    ):
        raise NotImplementedError


class Newton(FunctionSolver):
    def __init__(
        self,
        newton_epsilon: float,
        max_iterations: int,
    ):
        self.newton_epsilon = newton_epsilon
        self.max_iterations = max_iterations


class NewtonPlainPython(Newton):

    def solve(self, func, jacobian, initial):

        # Newton iteration starts
        residual_norm = 1e5
        index_iteration = 0

        # Iterate while residual isnt zero and max. iterations number isnt reached
        while (residual_norm >= self.newton_epsilon) and (
            index_iteration < self.max_iterations
        ):
            index_iteration += 1
            residual = func(initial)
            tangent_matrix = jacobian(initial)
            state_delta = -np.linalg.inv(tangent_matrix) @ residual
            initial = initial + state_delta
            residual_norm = np.linalg.norm(residual)
            utils.print_residual_norm(value=residual_norm)

        if residual_norm < self.newton_epsilon:
            pass
        else:
            raise utils.PydykitException("Newton convergence not succesful")

        return initial


class NewtonScipy(Newton):
    def solve(self, func, jacobian, initial):
        # TODO: Log the logs of the optimization function
        return root(
            fun=func,
            x0=initial,
            jac=jacobian,
            tol=self.newton_epsilon,
            # maxiter=self.max_iterations,
        ).x
