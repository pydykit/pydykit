import abc
from collections import namedtuple
from typing import Iterator


class PortHamiltonianIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        raise NotImplementedError


class MultiBodyIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        raise NotImplementedError


class Solver(abc.ABC):

    def __init__(self, manager, newton_epsilon: float, max_iterations: int):
        self.manager = manager
        self.newton_epsilon = newton_epsilon
        self.max_iterations = max_iterations

    @abc.abstractmethod
    def solve(self, state_initial):
        raise NotImplementedError


class AbstractMultiBodySystem(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def decompose_state(self):
        raise NotImplementedError

    @abc.abstractmethod
    def mass_matrix(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def inverse_mass_matrix(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def kinetic_energy(self, q, p):
        raise NotImplementedError

    @abc.abstractmethod
    def kinetic_energy_gradient_from_momentum(self, q, p):
        raise NotImplementedError

    @abc.abstractmethod
    def kinetic_energy_gradient_from_velocity(self, q, v):
        raise NotImplementedError

    @abc.abstractmethod
    def external_potential(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def external_potential_gradient(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def internal_potential(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def internal_potential_gradient(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def potential_energy(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def potential_energy_gradient(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def total_energy(self, q, p):
        raise NotImplementedError

    @abc.abstractmethod
    def constraint(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def constraint_gradient(self, q):
        raise NotImplementedError

    @abc.abstractmethod
    def constraint_velocity(self, q, p):
        raise NotImplementedError

    @abc.abstractmethod
    def dissipation_matrix(self, q, v):
        raise NotImplementedError

    @abc.abstractmethod
    def rayleigh_dissipation(self, q, v):
        raise NotImplementedError


class AbstractPortHamiltonianSystem(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def decompose_state(self):
        raise NotImplementedError

    @abc.abstractmethod
    def costates(self, state):
        raise NotImplementedError

    @abc.abstractmethod
    def hamiltonian(self, state):
        raise NotImplementedError

    @abc.abstractmethod
    def hamiltonian_gradient(self, state):
        raise NotImplementedError

    @abc.abstractmethod
    def structure_matrix(self):
        raise NotImplementedError

    @abc.abstractmethod
    def descriptor_matrix(self, state):
        raise NotImplementedError

    @abc.abstractmethod
    def dissipation_matrix(self, state):
        raise NotImplementedError

    @abc.abstractmethod
    def port_matrix(self, state):
        raise NotImplementedError

    @abc.abstractmethod
    def input(self):
        raise NotImplementedError

    @abc.abstractmethod
    def output(self, state):
        raise NotImplementedError


class TimeStep:
    def __init__(self, index: int, time: float, increment: float):
        self.index = index
        self.time = time
        self.increment = (
            increment  # this is next point in time minus current point in time
        )


class TimeStepper(abc.ABC):
    def __init__(self, manager, step_size: float, start: float, end: float):
        self.manager = manager
        self.step_size = step_size
        self.start = start
        self.end = end

    @abc.abstractmethod
    def make_steps(self) -> Iterator[TimeStep]:
        """Returns a Python generator which returns TimeStep objects"""

    @property
    @abc.abstractmethod
    def current_step(self) -> TimeStep:
        raise NotImplementedError
