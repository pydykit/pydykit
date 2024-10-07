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
