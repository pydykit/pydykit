import abc
from collections import namedtuple

import numpy as np

from . import operators, states


class PortHamiltonianSystem(abc.ABC):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

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

    def decompose_state(self, state):
        decomposed_state = namedtuple("state", "q v")
        return decomposed_state(
            q=state[0],
            v=state[1],
        )

    def compose_state(self):
        pass

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


class MultiBodySystem(abc.ABC):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

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
            ],  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator?
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
        return 0.5 * (q.T @ q / self.length**2 - 1.0)

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
        return operators.combine_G_inertias(
            g_matrix=G_q,
            inertias=self.inertias_matrix,
        )

    def kinetic_energy_gradient_from_momentum(self, q, p):
        return np.zeros(3)

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
        return np.zeros(3)

    def constraint(self, q):
        return 0.5 * (q.T @ q - 1.0)

    def constraint_gradient(self, q):
        return q.T
