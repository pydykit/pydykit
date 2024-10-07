import abc
from collections import namedtuple


class PortHamiltonianIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        pass


class MultiBodyIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        pass


class Solver(abc.ABC):

    def __init__(self, manager, newton_epsilon: float, max_iterations: int):
        self.manager = manager
        self.newton_epsilon = newton_epsilon
        self.max_iterations = max_iterations

    @abc.abstractmethod
    def solve(self, state_initial):
        pass
