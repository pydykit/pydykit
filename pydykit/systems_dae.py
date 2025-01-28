"""
My system DAE module

This module contains the system classes DAE.

Classes:
    QuasiLinearDAESystem: A class quasilinear DAE systems.
    ChemicalReactor: A chemical reactor system.
"""

import numpy as np

from . import abstract_base_classes
from .systems import System


class QuasiLinearDAESystem(System, abstract_base_classes.AbstractQuasiLinearDAESystem):
    r"""
    These systems follow the pattern:

    $$
       E(x) \dot{x} = f(x)
    $$

    where $x$: state, $E$: descriptor matrix, $f$: right-hand side and $\nabla f(x)$: Jacobian.

    It includes ODEs for $E(x) = I$. Singular $E$ induce true DAEs.
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
                [
                    state[0],
                    state[1],
                    state[2],
                ],
            )
        )

    def get_state_columns(self):
        return [
            "x",
            "y",
            "z",
        ]

    def right_hand_side(self):
        state = self.decompose_state()
        x = state["x"]
        y = state["y"]
        z = state["z"]

        return np.array(
            [
                self.sigma * (y - x),
                x * (self.rho - z) - y,
                x * y - self.beta * z,
            ]
        )

    def jacobian(self):
        state = self.decompose_state()
        x = state["x"]
        y = state["y"]
        matrix = np.array(
            [
                [-self.sigma, self.sigma, 0],
                [self.rho, -1, -x],
                [y, x, -self.beta],
            ]
        )
        return matrix

    def descriptor_matrix(self):
        return np.eye(3)


class ChemicalReactor(QuasiLinearDAESystem):
    """
    Follows the equations described in the following references:

    References
    ----------
    1. https://doi.org/10.1137/0909014, Eq. 33a
    2. https://doi.org/10.4171/017, Eq. 1.8
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
                [
                    state[0],
                    state[1],
                    state[2],
                ],
            )
        )

    def get_state_columns(self):
        return [
            "concentration",
            "temperature",
            "reaction_rate",
        ]

    def descriptor_matrix(self):
        return np.diag((1, 1, 0))

    def right_hand_side(self):
        state = self.decompose_state()
        c = state["concentration"]
        T = state["temperature"]
        R = state["reaction_rate"]

        k1, k2, k3, k4 = self.constants
        TC = self.cooling_temperature
        c0 = self.reactant_concentration
        T0 = self.initial_temperature

        rhs = np.array(
            [
                k1 * (c0 - c) - R,
                k1 * (T0 - T) + k2 * R - k3 * (T - TC),
                R - k3 * np.exp(-k4 / T) * c,
            ]
        )

        return rhs

    def jacobian(self):
        state = self.decompose_state()
        c = state["concentration"]
        T = state["temperature"]

        k1, k2, k3, k4 = self.constants

        matrix = np.array(
            [
                [-k1, 0, -1],
                [0, -(k1 + k3), k2],
                [-k3 * np.exp(-k4 / T), k3 * np.exp(-k4 / T) * k4 / (T**2) * c, 1],
            ]
        )
        return matrix
