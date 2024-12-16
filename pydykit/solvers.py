import numpy as np
from scipy.optimize import fsolve

from . import abstract_base_classes, utils


class Iterative(abstract_base_classes.Solver):

    def __init__(
        self,
        newton_epsilon: float,
        max_iterations: int,
    ):
        self.newton_epsilon = newton_epsilon
        self.max_iterations = max_iterations
        self.has_failed = False


class NewtonPlainPython(Iterative):

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
            print("Newton convergence not succesful!")
            self.has_failed = True

        return initial


class RootScipy(Iterative):
    def solve(self, func, jacobian, initial):

        self.func = func

        solution = fsolve(
            func=func,
            x0=initial,
            fprime=jacobian,
            xtol=self.newton_epsilon,
        )

        residual_norm = np.linalg.norm(func(solution))
        utils.print_residual_norm(value=residual_norm)

        return solution
