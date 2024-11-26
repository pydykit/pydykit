import abc
from typing import Callable, Iterator

import numpy as np
import numpy.typing as npt

from . import results


class Integrator(abc.ABC):

    @abc.abstractmethod
    def __init__(self, manager):
        pass

    @abc.abstractmethod
    def get_residuum(self, state):
        pass

    @abc.abstractmethod
    def get_tangent(self, state):
        pass


class Simulator(abc.ABC):

    @abc.abstractmethod
    def run(self):
        pass


class Solver(abc.ABC):

    @abc.abstractmethod
    def solve(
        self,
        func: Callable,
        jacobian: Callable,
        initial: npt.ArrayLike,
    ):
        pass


class System(abc.ABC):
    pass


class AbstractMultiBodySystem(System):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def mass_matrix(self):
        pass

    @abc.abstractmethod
    def inverse_mass_matrix(self):
        pass

    @abc.abstractmethod
    def kinetic_energy(self):
        pass

    @abc.abstractmethod
    def kinetic_energy_gradient_from_momentum(self):
        pass

    @abc.abstractmethod
    def kinetic_energy_gradient_from_velocity(self):
        pass

    @abc.abstractmethod
    def external_potential(self):
        pass

    @abc.abstractmethod
    def external_potential_gradient(self):
        pass

    @abc.abstractmethod
    def internal_potential(self):
        pass

    @abc.abstractmethod
    def internal_potential_gradient(self):
        pass

    @abc.abstractmethod
    def potential_energy(self):
        pass

    @abc.abstractmethod
    def potential_energy_gradient(self):
        pass

    @abc.abstractmethod
    def total_energy(self):
        pass

    @abc.abstractmethod
    def constraint(self):
        pass

    @abc.abstractmethod
    def constraint_gradient(self):
        pass

    @abc.abstractmethod
    def constraint_velocity(self):
        pass

    @abc.abstractmethod
    def dissipation_matrix(self):
        pass

    @abc.abstractmethod
    def rayleigh_dissipation(self):
        pass


class AbstractPortHamiltonianSystem(System):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def costates(self):
        pass

    @abc.abstractmethod
    def hamiltonian(self):
        pass

    @abc.abstractmethod
    def hamiltonian_gradient(self):
        pass

    @abc.abstractmethod
    def structure_matrix(self):
        pass

    @abc.abstractmethod
    def descriptor_matrix(self):
        pass

    @abc.abstractmethod
    def dissipation_matrix(self):
        pass

    @abc.abstractmethod
    def port_matrix(self, state):
        pass

    @abc.abstractmethod
    def input_vector(self):
        pass

    @abc.abstractmethod
    def output(self):
        pass


class AbstractQuasiLinearDAESystem(System):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def get_state_columns(self):
        pass

    @abc.abstractmethod
    def right_hand_side(self):
        pass

    @abc.abstractmethod
    def descriptor_matrix(self):
        pass


class TimeStep(abc.ABC):
    pass


class TimeStepper(abc.ABC):

    @abc.abstractmethod
    def make_steps(self) -> Iterator[TimeStep]:
        pass

    @property
    @abc.abstractmethod
    def current_step(self) -> TimeStep:
        pass


class Manager(abc.ABC):
    time_stepper: TimeStepper = NotImplemented
    simulator: Simulator = NotImplemented
    integrator: Integrator = NotImplemented
    system: System = NotImplemented
    result: results.Result = NotImplemented


class DiscreteGradient(abc.ABC):
    """Abstract base class for discrete gradient computation."""

    @abc.abstractmethod
    def compute(
        self,
        system_n,
        system_n1,
        system_n05,
        func_name: str,
        jacobian_name: str,
        argument_n: np.ndarray,
        argument_n1: np.ndarray,
        **kwargs,
    ) -> np.ndarray:
        """Compute the discrete gradient."""
        pass
