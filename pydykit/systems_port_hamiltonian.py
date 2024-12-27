import numpy as np
from scipy.linalg import block_diag

from . import abstract_base_classes, utils
from .systems import System


class PortHamiltonianSystem(
    abstract_base_classes.AbstractPortHamiltonianSystem,
    System,  # TODO: Avoid multi-inheritance if possible
):
    """
    These systems follow the pattern:
    E(x) dot{x} = (J(x)-R(x))z(x) + B(x)u
     E(x)^T z(x) = \nabla H(x)
               y = B(x)^T z(x)
    where x: state
          E: descriptor matrix
          J: structure matrix
          R: dissipation matrix
          z: co-state
          B: port matrix
          u: input vector
          H: Hamiltonian
          y: output
          \nabla H(x): Hamiltonian gradient
    It includes ODEs for E(x) = I. Singular E induce true DAEs.
    """

    def __init__(self, manager, state):
        self.manager = manager
        self.initialize_state(state)
        self.parametrization = ["state"]
        self.composed_hamiltonian = False

    def output(self):
        return self.port_matrix.T @ self.input_vector()


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
        self.mass = mass
        self.gravity = gravity
        self.length = length

    def get_state_columns(self):
        return ["angle", "angular_velocity"]

    def decompose_state(self):
        state = self.state
        assert len(state) == 2
        return dict(
            zip(
                self.get_state_columns(),
                [state[0], state[1]],
            )
        )

    def costates(self):
        q = self.decompose_state()["angle"]
        v = self.decompose_state()["angular_velocity"]
        return np.array([self.mass * self.gravity * self.length * np.sin(q), v])

    def get_algebraic_costate(self):
        return []

    def hamiltonian(self):
        q = self.decompose_state()["angle"]
        v = self.decompose_state()["angular_velocity"]
        return (
            -self.mass * self.gravity * self.length * np.cos(q)
            + 0.5 * self.mass * self.length**2 * v**2
        )

    def hamiltonian_gradient(self):
        q = self.decompose_state()["angle"]
        v = self.decompose_state()["angular_velocity"]
        return np.array(
            [
                self.mass * self.gravity * self.length * np.sin(q),
                self.mass * self.length**2 * v,
            ]
        )

    def hamiltonian_differential_gradient(self):
        return self.hamiltonian_gradient()

    def structure_matrix(self):
        return np.array([[0, 1], [-1, 0]])

    def descriptor_matrix(self):
        return np.diag([1, self.mass * self.length**2])

    def nonsingular_descriptor_matrix(self):
        return self.descriptor_matrix()

    def port_matrix(self):
        pass

    def input_vector(self):
        pass

    def dissipation_matrix(self):
        return np.zeros([2, 2])


class PortHamiltonianMBS(PortHamiltonianSystem):

    def __init__(self, manager):
        self.mbs = manager.system
        super().__init__(manager, state=manager.system.initial_state)
        self.parametrization = ["state"]
        self.composed_hamiltonian = True
        self.nbr_hamiltonian_parts = 2
        self.differential_state_composition = ["position", "momentum"]

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
                decomposed_state["momentum"],
                decomposed_state["multiplier"],
            ]
        )

    def hamiltonian_gradient(self):
        decomposed_state = self.decompose_state()
        v = decomposed_state["momentum"]
        lambd = decomposed_state["multiplier"]
        dim_lambd = len(lambd)
        mass_matrix = self.mbs.mass_matrix()

        return np.concatenate(
            [
                self.mbs.external_potential_gradient()
                + self.mbs.internal_potential_gradient(),
                mass_matrix @ v,
                np.zeros(dim_lambd),
            ],
            axis=0,
        )

    def hamiltonian_differential_gradient(self):
        return np.concatenate(
            [
                self.hamiltonian_differential_gradient_1(),
                self.hamiltonian_differential_gradient_2(),
            ],
            axis=0,
        )

    def hamiltonian_differential_gradient_1(self):

        return (
            self.mbs.external_potential_gradient()
            + self.mbs.internal_potential_gradient()
        )

    def hamiltonian_differential_gradient_2(self):
        decomposed_state = self.decompose_state()
        v = decomposed_state["momentum"]
        mass_matrix = self.mbs.mass_matrix()

        return mass_matrix @ v

    def structure_matrix(self):
        decomposed_state = self.decompose_state()
        q = decomposed_state["position"]
        v = decomposed_state["momentum"]
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

    def nonsingular_descriptor_matrix(self):
        identity_mat = np.eye(self.mbs.nbr_dof)
        mass_matrix = self.mbs.mass_matrix()

        return block_diag(identity_mat, mass_matrix)

    def hamiltonian(self):
        return self.hamiltonian_1() + self.hamiltonian_2()

    def hamiltonian_1(self):
        return self.mbs.external_potential() + self.mbs.internal_potential()

    def hamiltonian_2(self):
        decomposed_state = self.decompose_state()
        v = decomposed_state["momentum"]
        return 0.5 * np.dot(v, self.mbs.mass_matrix() @ v)

    def port_matrix(self):
        pass

    def input_vector(self):
        pass

    def dissipation_matrix(self):
        zeros_matrix_1 = np.zeros([self.mbs.nbr_dof, self.mbs.nbr_dof])
        diss_mat = self.mbs.dissipation_matrix()
        zeros_matrix_2 = np.zeros((self.mbs.nbr_constraints, self.mbs.nbr_constraints))
        ph_dissipation_matrix = block_diag(zeros_matrix_1, diss_mat, zeros_matrix_2)

        return ph_dissipation_matrix

    def dissipated_power(self):
        return np.dot(self.costates(), self.dissipation_matrix() @ self.costates())

    def get_algebraic_costate(self):
        decomposed_state = self.decompose_state()
        lambd = decomposed_state["multiplier"]
        return lambd

    def get_differential_state(self):
        decomposed_state = self.decompose_state()
        q = decomposed_state["position"]
        v = decomposed_state["momentum"]
        return np.concatenate([q, v], axis=0)

    def constraint(self):
        return self.mbs.constraint()

    def constraint_velocity(self):
        decomposed_state = self.decompose_state()
        v = decomposed_state["momentum"]
        return self.mbs.constraint_gradient() @ v
