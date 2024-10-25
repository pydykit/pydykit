import copy

import numpy as np

from .. import utils


class System:
    # inspired by mixin classes approach
    def copy(self, state):
        new = copy.deepcopy(self)
        new.state = state
        return new


class GeneralODESystem(
    System,
):
    def __init__(self, manager, state):
        self.manager = manager
        self.initialize_state(state)

    def initialize_state(self, state):

        # convert state as dict to array with values
        self.initial_state = state
        self.dim_state = utils.get_nbr_elements_dict_list(self.initial_state)
        self.parametrization = ["state"]
        self.state_columns = self.get_state_columns()
        self.build_state_vector()

    def build_state_vector(self):
        self.state = np.hstack(list(self.initial_state.values()))

    def get_state_columns(self):
        pass


class Lorenz(GeneralODESystem):
    def __init__(self, manager, state, sigma, rho, beta):
        super().__init__(manager, state)
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def decompose_state(self):
        state = self.state
        assert len(state) == 3
        return dict(
            zip(
                self.get_state_columns(),
                [state[0], state[1], state[2]],
            )
        )

    def get_state_columns(self):
        return ["x", "y", "z"]

    def right_hand_side(self):
        x = self.decompose_state()["x"]
        y = self.decompose_state()["y"]
        z = self.decompose_state()["z"]

        return np.array(
            [self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z]
        )

    def jacobian(self):
        x = self.decompose_state()["x"]
        y = self.decompose_state()["y"]
        matrix = np.array(
            [[-self.sigma, self.sigma, 0], [self.rho, -1, -x], [y, x, -self.beta]]
        )
        return matrix
