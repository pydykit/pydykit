import abc
from collections import namedtuple

import numpy as np

from . import states, utils


class System(abc.ABC):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    @abc.abstractmethod
    def get_z_vector(self, state):
        pass

    @abc.abstractmethod
    def get_jacobian(self, state):
        pass

    @abc.abstractmethod
    def get_j_matrix(self):
        pass

    @abc.abstractmethod
    def get_e_matrix(self, state):
        pass

    @abc.abstractmethod
    def initialize(self):
        pass


class Pendulum2D(System):

    def decompose_state(self, state):
        decomposed_state = namedtuple("state", "q v")
        return decomposed_state(
            q=state[0],
            v=state[1],
        )

    def get_z_vector(self, state):
        q, v = self.decompose_state(state=state)
        return np.array([self.mass * self.gravity * self.length * np.sin(q), v])

    def get_jacobian(self, state):
        q, v = self.decompose_state(state=state)
        return np.diag([self.mass * self.gravity * self.length * np.cos(q), 1])

    def get_j_matrix(self):
        return np.array([[0, 1], [-1, 0]])

    def get_e_matrix(self, state):
        return np.diag([1, self.mass * self.length**2])

    def initialize(self):
        self.states = states.States(
            nbr_states=self.manager.time_stepper.nbr_timesteps + 2,
            dim_state=2,
        )
        self.states.state_n = self.states.state_n1 = self.states.state[0, :] = np.array(
            self.initial_state
        )
