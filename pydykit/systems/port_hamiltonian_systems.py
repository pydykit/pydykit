import abc

import numpy as np
from scipy.linalg import block_diag

from .. import base_classes, utils
from .system import System


class PortHamiltonianSystem(
    base_classes.AbstractPortHamiltonianSystem,
    System,  # TODO: Avoid multi-inheritance if possible
):
    def __init__(self, manager, state):
        self.manager = manager
        self.initialize_state(state)

    def initialize_state(self, state):

        # convert state as dict to array with values
        self.initial_state = state
        self.dim_state = utils.get_nbr_elements_dict_list(self.initial_state)
        self.state_names = utils.get_keys_dict_list(self.initial_state)
        self.state_columns = self.get_state_columns()
        self.build_state_vector()

    def build_state_vector(self):
        self.state = np.hstack(list(self.initial_state.values()))

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def costates(self, state):
        pass

    @abc.abstractmethod
    def hamiltonian(self, state):
        pass

    @abc.abstractmethod
    def hamiltonian_gradient(self, state):
        pass

    @abc.abstractmethod
    def structure_matrix(self):
        pass

    @abc.abstractmethod
    def descriptor_matrix(self, state):
        pass

    @abc.abstractmethod
    def dissipation_matrix(self, state):
        pass

    @abc.abstractmethod
    def port_matrix(self, state):
        pass

    @abc.abstractmethod
    def input(self):
        pass

    def output(self, state):
        return self.port_matrix.T @ self.input(state)


class Pendulum2D(PortHamiltonianSystem):

    def __init__(
        self,
        manager,
        state,
        mass: float,
        gravity: float,
        length: float,
    ):

        super().__init__(manager, state)
        self.mass = 1.0
        self.gravity = 9.81
        self.length = 1.0

    def get_state_columns(self):
        return self.state_names  # special case!

    def decompose_state(self):
        state = self.state
        assert len(state) == 2
        return dict(
            zip(
                self.state_names,
                [state[0], state[1]],
            )
        )

    def costates(self):
        q = self.decompose_state()["position"]
        v = self.decompose_state()["velocity"]
        return np.array([self.mass * self.gravity * self.length * np.sin(q), v])

    def hamiltonian(self):
        pass

    def hamiltonian_gradient(self):
        q = self.decompose_state()["position"]
        return np.diag([self.mass * self.gravity * self.length * np.cos(q), 1])

    def structure_matrix(self):
        return np.array([[0, 1], [-1, 0]])

    def descriptor_matrix(self):
        return np.diag([1, self.mass * self.length**2])

    def port_matrix(self):
        pass

    def input(self):
        pass

    def dissipation_matrix(self):
        pass


class PortHamiltonianMBS(PortHamiltonianSystem):

    def __init__(self, manager):
        self.mbs = manager.system
        super().__init__(manager, state=manager.system.initial_state)

    def copy(self, state):
        system = super().copy(state=state)
        system.mbs.state = state
        return system

    def get_state_dimensions(self):
        return self.mbs.get_state_dimensions()

    def get_state_columns(self):
        return self.mbs.get_state_columns()

    def decompose_state(self):
        return self.mbs.decompose_state()

    def costates(self):
        decomposed_state = self.decompose_state()
        potential_forces = (
            self.mbs.external_potential_gradient()
            + self.mbs.internal_potential_gradient()
        )

        return np.hstack(
            [
                potential_forces,
                decomposed_state["velocity"],
                decomposed_state["multiplier"],
            ]
        )

    def hamiltonian_gradient(self):
        return (
            self.mbs.external_potential_gradient()
            + self.mbs.internal_potential_gradient()
        )

    def structure_matrix(self):
        decomposed_state = self.decompose_state()
        q = decomposed_state["position"]
        v = decomposed_state["velocity"]
        lambd = decomposed_state["multiplier"]
        G = self.mbs.constraint_gradient()

        return np.block(
            [
                [
                    np.zeros((len(q), len(q))),
                    np.eye(len(q)),
                    np.zeros((len(q), len(lambd))),
                ],
                [-np.eye(len(v)), np.zeros((len(v), len(v))), -G.T],
                [np.zeros((len(lambd), len(q))), G, np.zeros((len(lambd), len(lambd)))],
            ]
        )

    def descriptor_matrix(self):
        identity_mat = np.eye(self.mbs.nbr_dof)
        mass_matrix = self.mbs.mass_matrix()
        zeros_matrix = np.zeros((self.mbs.nbr_constraints, self.mbs.nbr_constraints))
        descriptor_matrix = block_diag(identity_mat, mass_matrix, zeros_matrix)

        return descriptor_matrix

    def hamiltonian(self):
        pass

    def port_matrix(self):
        pass

    def input(self):
        pass

    def dissipation_matrix(self):
        pass
