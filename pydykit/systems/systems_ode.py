import numpy as np

from .. import utils
from .system import System


class GeneralODESystem(
    System,
):
    def __init__(self, manager, state):
        self.manager = manager
        self.initialize_state(state)
        self.parametrization = ["state"]

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
