import abc
from collections import namedtuple

import numpy as np

from scipy.linalg import block_diag

from . import operators, states, utils


class PortHamiltonianSystem(abc.ABC):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)
        self.already_initialized = False

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def compose_state(self):
        pass

    @abc.abstractmethod
    def get_costates(self, state):
        pass

    @abc.abstractmethod
    def get_hamiltonian_gradient(self, state):
        pass

    @abc.abstractmethod
    def get_structure_matrix(self):
        pass

    @abc.abstractmethod
    def get_descriptor_matrix(self, state):
        pass


class Pendulum2D(PortHamiltonianSystem):

    def initialize(self):

        self.states = states.State(
            nbr_states=self.manager.time_stepper.nbr_time_points,
            dim_state=2,
            columns=["angle", "velocity"],
        )
        self.states.state_n = self.states.state_n1 = self.states.state[0, :] = np.array(
            self.initial_state
        )

        self.already_initialized = True

    def decompose_state(self, state):
        decomposed_state = namedtuple("state", "q v")
        return decomposed_state(
            q=state[0],
            v=state[1],
        )

    def compose_state(self):
        pass

    def get_costates(self, state):
        q, v = self.decompose_state(state=state)
        return np.array([self.mass * self.gravity * self.length * np.sin(q), v])

    def get_hamiltonian_gradient(self, state):
        q, v = self.decompose_state(state=state)
        return np.diag([self.mass * self.gravity * self.length * np.cos(q), 1])

    def get_structure_matrix(self, state):
        return np.array([[0, 1], [-1, 0]])

    def get_descriptor_matrix(self, state):
        return np.diag([1, self.mass * self.length**2])


class PortHamiltonianMBS(PortHamiltonianSystem):

    def initialize(self, MultiBodySystem):

        self.MBS = MultiBodySystem

        self.states = MultiBodySystem.states

        self.already_initialized = True

    def decompose_state(self, state):
        utils.pydykitException("not implemented")
        pass

    def compose_state(self):
        utils.pydykitException("not implemented")
        pass

    def get_costates(self, state):
        decomposed_state = self.MBS.decompose_state(state)
        potential_forces = self.MBS.external_potential_gradient(
            decomposed_state.q
        ) + self.MBS.internal_potential_gradient(decomposed_state.q)

        return np.hstack([potential_forces, decomposed_state.p, decomposed_state.lambd])

    def get_hamiltonian_gradient(self, state):
        decomposed_state = self.MBS.decompose_state(state)

        return self.MBS.external_potential_gradient(
            decomposed_state.q
        ) + self.MBS.internal_potential_gradient(decomposed_state.q)

    def get_structure_matrix(self, state):
        decomposed_state = self.MBS.decompose_state(state)
        q = decomposed_state.q
        v = decomposed_state.p
        lambd = decomposed_state.lambd
        G = self.MBS.constraint_gradient(q)

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

    def get_descriptor_matrix(self, state):
        identity_mat = np.eye(self.MBS.nbr_dof)
        decomposed_state = self.MBS.decompose_state(state)
        mass_matrix = self.MBS.get_mass_matrix(decomposed_state.q)
        zeros_matrix = np.zeros((self.MBS.nbr_constraints, self.MBS.nbr_constraints))
        descriptor_matrix = block_diag(identity_mat, mass_matrix, zeros_matrix)

        return descriptor_matrix


class MultiBodySystem(abc.ABC):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)
        self.already_initialized = False

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def compose_state(self):
        pass

    @abc.abstractmethod
    def get_mass_matrix(self, q):
        pass

    @abc.abstractmethod
    def kinetic_energy_gradient_from_momentum(self, q, p):
        "q:position, p:momentum"
        pass

    @abc.abstractmethod
    def kinetic_energy_gradient_from_velocity(self, q, v):
        "v: velocity"
        # Note: A given integrator needs kinetic_energy_gradient_from_momentum or kinetic_energy_gradient_from_velocity, not both
        pass

    @abc.abstractmethod
    def external_potential(self, q):
        pass

    @abc.abstractmethod
    def external_potential_gradient(self, q):
        pass

    @abc.abstractmethod
    def internal_potential(self, q):
        pass

    @abc.abstractmethod
    def internal_potential_gradient(self, q):
        pass

    @abc.abstractmethod
    def constraint(self, q):
        pass

    @abc.abstractmethod
    def constraint_gradient(self, q):
        pass


class Pendulum3DCartesian(MultiBodySystem):

    def initialize(self):
        self.length = np.linalg.norm(self.initial_state["Q"])
        self.ext_acc = np.array(self.ext_acc)

        self.states = states.State(
            nbr_states=self.manager.time_stepper.nbr_time_points,
            dim_state=2 * self.nbr_spatial_dimensions + self.nbr_constraints,
            columns=[
                "x",
                "y",
                "z",
                "dx",
                "dy",
                "dz",
                "lambda",
            ],  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!
        )

        self.states.state_n = self.states.state_n1 = self.states.state[0, :] = (
            self.compose_state(
                q=np.array(self.initial_state["Q"]),
                p=self.get_mass_matrix(q=None) @ np.array(self.initial_state["V"]),
                lambd=np.zeros(self.nbr_constraints),
            )
        )

    def decompose_state(self, state):
        dim = self.nbr_spatial_dimensions

        assert len(state) == 2 * dim + self.nbr_constraints

        decomposed_state = namedtuple("state", "q p lambd")
        return decomposed_state(
            q=state[0:dim],
            p=state[dim : 2 * dim],
            lambd=state[2 * dim :],
        )

    def compose_state(self, q, p, lambd):
        return np.concatenate(
            [
                q,
                p,
                lambd,
            ],
            axis=0,
        )

    def get_mass_matrix(self, q):
        return self.mass * np.eye(self.nbr_spatial_dimensions)

    def kinetic_energy_gradient_from_momentum(self, q, p):
        return np.zeros(q.shape)

    def kinetic_energy_gradient_from_velocity(self, q, v):
        return np.zeros(q.shape)

    def external_potential(self, q):
        return -(self.get_mass_matrix(q=q) @ self.ext_acc).T @ q

    def external_potential_gradient(self, q):
        return -self.get_mass_matrix(q=q) @ self.ext_acc

    def internal_potential(self):
        return 0.0

    def internal_potential_gradient(self, q):
        return np.zeros(q.shape)

    def constraint(self, q):
        return np.array([0.5 * (q.T @ q / self.length**2 - 1.0)])

    def constraint_gradient(self, q):
        return q.T[np.newaxis, :] / self.length**2


# operators


class RigidBodyRotatingQuaternions(MultiBodySystem):

    def initialize(self):
        self.inertias_matrix = np.diag(self.inertias)

        self.ext_acc = np.array(self.ext_acc)

        self.states = states.State(
            nbr_states=self.manager.time_stepper.nbr_time_points,
            dim_state=2 * self.nbr_dof + self.nbr_constraints,
            columns=[
                "q0",
                "q1",
                "q2",
                "q3",
                "q4",
                "p0",
                "p1",
                "p2",
                "p3",
                "p4",
                "lambda",
            ],  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!
        )
        q0 = np.array(self.initial_state["Q"])
        G_q0 = operators.get_convective_transformation_matrix(quat=q0)
        v0 = 0.5 * G_q0.T @ np.array(self.initial_state["V"])

        self.states.state_n = self.states.state_n1 = self.states.state[0, :] = (
            self.compose_state(
                q=q0,
                p=self.get_mass_matrix(q=np.array(self.initial_state["Q"])) @ v0,
                lambd=np.zeros(self.nbr_constraints),
            )
        )

    def decompose_state(self, state):

        assert len(state) == 2 * self.nbr_dof + self.nbr_constraints

        decomposed_state = namedtuple("state", "q p lambd")
        return decomposed_state(
            q=state[0 : self.nbr_dof],
            p=state[self.nbr_dof : 2 * self.nbr_dof],
            lambd=state[2 * self.nbr_dof :],
        )

    def compose_state(self, q, p, lambd):
        return np.concatenate(
            [
                q,
                p,
                lambd,
            ],
            axis=0,
        )

    def get_mass_matrix(self, q):
        quat = q[0:4]
        G_q = operators.get_convective_transformation_matrix(
            quat=quat,
        )

        singular_mass_matrix = 4.0 * G_q.T @ self.inertias_matrix @ G_q
        regular_mass_matrix = singular_mass_matrix + 2 * np.trace(
            self.inertias_matrix
        ) * np.outer(quat, quat)

        return regular_mass_matrix

    def get_inverse_mass_matrix(self, q):
        quat = q[0:4]
        Ql_q = operators.get_left_multiplation_matrix(quat)
        J0 = 0.5 * np.trace(self.inertias_matrix)
        inverse_inertias = 1.0 / np.diag(self.inertias_matrix)
        inverse_extended_inertias_matrix = np.diag(np.append(1 / J0, inverse_inertias))

        return 0.25 * Ql_q @ inverse_extended_inertias_matrix @ Ql_q.T

    def kinetic_energy_gradient_from_momentum(self, q, p):

        # extended inertia tensor
        J0 = np.trace(self.inertias_matrix)
        extended_inertias = np.block(
            [[J0, np.zeros((1, 3))], [np.zeros((3, 1)), self.inertias_matrix]]
        )

        inverse_extended_inertias = np.linalg.inv(extended_inertias)

        Ql_p = operators.get_left_multiplation_matrix(p)

        return 0.25 * Ql_p @ inverse_extended_inertias @ Ql_p.T @ q

    def kinetic_energy_gradient_from_velocity(self, q, v):
        tmp = v[:4]

        G_v = operators.get_convective_transformation_matrix(
            quat=tmp,
        )
        M_4_hat = operators.combine_G_inertias(
            g_matrix=G_v,
            inertias=self.inertias_matrix,
        )

        return M_4_hat @ q

    def external_potential(self, q):
        return 0.0

    def external_potential_gradient(self, q):
        return np.zeros(4)

    def internal_potential(self):
        return 0.0

    def internal_potential_gradient(self, q):
        return np.zeros(4)

    def constraint(self, q):
        return np.array([0.5 * (q.T @ q - 1.0)])

    def constraint_gradient(self, q):
        return q.T[np.newaxis, :]


class FourParticleSystem(MultiBodySystem):
    def initialize(self):

        self.ext_acc = np.repeat(self.ext_acc, repeats=4, axis=0)

        self.states = states.State(
            nbr_states=self.manager.time_stepper.nbr_time_points,
            dim_state=2 * self.nbr_spatial_dimensions * 4 + self.nbr_constraints,
            columns=[
                "x1",
                "y1",
                "z1",
                "x2",
                "y2",
                "z2",
                "x3",
                "y3",
                "z3",
                "x4",
                "y4",
                "z4",
                "dx1",
                "dy1",
                "dz1",
                "dx2",
                "dy2",
                "dz2",
                "dx3",
                "dy3",
                "dz3",
                "dx4",
                "dy4",
                "dz4",
                "lambda1",
                "lambda2",
            ],  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!
        )

        self.states.state_n = self.states.state_n1 = self.states.state[0, :] = (
            self.compose_state(
                q=np.array(self.initial_state["Q"]),
                p=self.get_mass_matrix(q=None) @ np.array(self.initial_state["V"]),
                lambd=np.zeros(self.nbr_constraints),
            )
        )

    def decompose_state(self, state):
        dim = self.nbr_spatial_dimensions * 4

        assert len(state) == 2 * dim + self.nbr_constraints

        decomposed_state = namedtuple("state", "q p lambd")
        return decomposed_state(
            q=state[0:dim],
            p=state[dim : 2 * dim],
            lambd=state[2 * dim :],
        )

    def compose_state(self, q, p, lambd):
        return np.concatenate(
            [
                q,
                p,
                lambd,
            ],
            axis=0,
        )

    def get_mass_matrix(self, q):
        diagonal_elements = np.concatenate(
            (
                self.masses[0] * np.ones(self.nbr_spatial_dimensions),
                self.masses[1] * np.ones(self.nbr_spatial_dimensions),
                self.masses[2] * np.ones(self.nbr_spatial_dimensions),
                self.masses[3] * np.ones(self.nbr_spatial_dimensions),
            )
        )
        return np.diag(diagonal_elements)

    def kinetic_energy_gradient_from_momentum(self, q, p):
        return np.zeros(q.shape)

    def kinetic_energy_gradient_from_velocity(self, q, v):
        return np.zeros(q.shape)

    def external_potential(self, q):
        return -(self.get_mass_matrix(q=None) @ self.ext_acc).T @ q

    def external_potential_gradient(self, q):
        return -self.get_mass_matrix(q=None) @ self.ext_acc

    def internal_potential(self, q):
        q_1, q_2, q_3, q_4 = self.get_elements_for_all_masses(q)

        contribution_first_spring = (
            0.5
            * self.spring_stiffness_parameter_13
            * ((q_3 - q_1).T @ (q_3 - q_1) - self.natural_spring_length_13**2) ** 2
        )

        contribution_second_spring = (
            0.5
            * self.spring_stiffness_parameter_24
            * ((q_4 - q_2).T @ (q_4 - q_2) - self.natural_spring_length_24**2) ** 2
        )

        return contribution_first_spring + contribution_second_spring

    def internal_potential_gradient(self, q):
        q_1, q_2, q_3, q_4 = self.get_elements_for_all_masses(q)

        contribution_first_spring = (
            self.spring_stiffness_parameter_13
            * ((q_3 - q_1).T @ (q_3 - q_1) - self.natural_spring_length_13**2)
            * np.hstack([-2 * (q_3 - q_1), np.zeros(3), 2 * (q_3 - q_1), np.zeros(3)])
        )

        contribution_second_spring = (
            self.spring_stiffness_parameter_24
            * ((q_4 - q_2).T @ (q_4 - q_2) - self.natural_spring_length_24**2)
            * np.hstack([np.zeros(3), -2 * (q_4 - q_2), np.zeros(3), 2 * (q_4 - q_2)])
        )

        return contribution_first_spring + contribution_second_spring

    def constraint(self, q):
        q_1, q_2, q_3, q_4 = self.get_elements_for_all_masses(q)
        first_constraint = 0.5 * (
            (q_2 - q_1).T @ (q_2 - q_1) - self.rigid_constraint_length_12**2
        )
        second_constraint = 0.5 * (
            (q_4 - q_3).T @ (q_4 - q_3) - self.rigid_constraint_length_34**2
        )

        return np.hstack([first_constraint, second_constraint])

    def constraint_gradient(self, q):
        q_1, q_2, q_3, q_4 = self.get_elements_for_all_masses(q)

        first_constraint_gradient = np.hstack(
            [-(q_2 - q_1), (q_2 - q_1), np.zeros(3), np.zeros(3)]
        )
        second_constraint_gradient = np.hstack(
            [np.zeros(3), np.zeros(3), -(q_4 - q_3), (q_4 - q_3)]
        )
        return np.vstack([first_constraint_gradient, second_constraint_gradient])

    def get_element_for_mass(self, vector, no):

        assert len(vector) == 4 * self.nbr_spatial_dimensions

        return vector[
            (no - 1) * self.nbr_spatial_dimensions : no * self.nbr_spatial_dimensions
        ]

    def get_elements_for_all_masses(self, vector):

        return (
            self.get_element_for_mass(vector, 1),
            self.get_element_for_mass(vector, 2),
            self.get_element_for_mass(vector, 3),
            self.get_element_for_mass(vector, 4),
        )
