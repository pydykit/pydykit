import numpy as np

from . import abstract_base_classes
from .systems import System


class QuasiLinearDAESystem(System, abstract_base_classes.AbstractQuasiLinearDAESystem):
    """
    These systems follow the pattern:
    E(x) \dot{x} = f(x)
    where x: state
          E: descriptor matrix
          f: right-hand side
          \nabla f(x): Jacobian
    It includes ODEs for E(x) = I. Singular E induce true DAEs.
    """

    def __init__(self, manager, state: dict):
        self.manager = manager
        self.initialize_state(state)
        self.parametrization = ["state"]


class Lorenz(QuasiLinearDAESystem):
    def __init__(self, manager, state, sigma: float, rho: float, beta: float):
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

    def descriptor_matrix(self):
        return np.eye(3)


class ChemicalReactor(QuasiLinearDAESystem):
    """
    Follows [1] and [2].
    [1]: https://doi.org/10.1137/0909014 , Eq. 33a
    [2]: https://doi.org/10.4171/017 , Eq. 1.8
    """

    def __init__(
        self,
        manager,
        state,
        constants: list[float],
        cooling_temperature: float,
        reactant_concentration: float,
        initial_temperature: float,
    ):
        super().__init__(manager, state)
        self.constants = constants
        self.cooling_temperature = cooling_temperature
        self.reactant_concentration = reactant_concentration
        self.initial_temperature = initial_temperature

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
        return ["concentration", "temperature", "reaction_rate"]

    def descriptor_matrix(self):
        return np.diag((1, 1, 0))

    def right_hand_side(self):
        c = self.decompose_state()["concentration"]
        T = self.decompose_state()["temperature"]
        R = self.decompose_state()["reaction_rate"]

        k1, k2, k3, k4 = self.constants
        TC = self.cooling_temperature
        c0 = self.reactant_concentration
        T0 = self.initial_temperature

        RHS = np.array(
            [
                k1 * (c0 - c) - R,
                k1 * (T0 - T) + k2 * R - k3 * (T - TC),
                R - k3 * np.exp(-k4 / T) * c,
            ]
        )

        return RHS

    def jacobian(self):
        c = self.decompose_state()["concentration"]
        T = self.decompose_state()["temperature"]

        k1, k2, k3, k4 = self.constants

        matrix = np.array(
            [
                [-k1, 0, -1],
                [0, -(k1 + k3), k2],
                [-k3 * np.exp(-k4 / T), k3 * np.exp(-k4 / T) * k4 / (T**2) * c, 1],
            ]
        )
        return matrix
