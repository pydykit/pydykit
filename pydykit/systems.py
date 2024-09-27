import abc
from collections import namedtuple

import numpy as np
from scipy.linalg import block_diag

from . import managers, operators, states, utils


class AbstractMultiBodySystem(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def compose_state(self):
        pass

    @abc.abstractmethod
    def mass_matrix(self, q):
        pass

    @abc.abstractmethod
    def inverse_mass_matrix(self, q):
        pass

    @abc.abstractmethod
    def kinetic_energy(self, q, p):
        pass

    @abc.abstractmethod
    def kinetic_energy_gradient_from_momentum(self, q, p):
        pass

    @abc.abstractmethod
    def kinetic_energy_gradient_from_velocity(self, q, v):
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
    def potential_energy(self, q):
        pass

    @abc.abstractmethod
    def potential_energy_gradient(self, q):
        pass

    @abc.abstractmethod
    def total_energy(self, q, p):
        pass

    @abc.abstractmethod
    def constraint(self, q):
        pass

    @abc.abstractmethod
    def constraint_gradient(self, q):
        pass

    @abc.abstractmethod
    def constraint_velocity(self, q, p):
        pass

    @abc.abstractmethod
    def dissipation_matrix(self, q, v):
        pass

    @abc.abstractmethod
    def rayleigh_dissipation(self, q, v):
        pass


class MultiBodySystem(AbstractMultiBodySystem):
    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        nbr_constraints: int,
        nbr_dof: int,
        mass: float,
        gravity: list[float,],
    ):
        self.manager = manager
        self.nbr_spatial_dimensions = nbr_spatial_dimensions
        self.nbr_constraints = nbr_constraints
        self.nbr_dof = nbr_dof
        self.mass = mass
        self.gravity = gravity

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def compose_state(self):
        pass

    @abc.abstractmethod
    def mass_matrix(self, q):
        pass

    @abc.abstractmethod
    def inverse_mass_matrix(self, q):
        pass

    def kinetic_energy(self, q, p):
        return 0.5 * p.T @ self.inverse_mass_matrix(q=q) @ p

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

    def potential_energy(self, q):
        return self.external_potential(q) + self.internal_potential(q)

    def potential_energy_gradient(self, q):
        return self.external_potential_gradient(q=q) + self.internal_potential_gradient(
            q=q
        )

    def total_energy(self, q, p):
        return self.kinetic_energy(q, p) + self.potential_energy(q)

    @abc.abstractmethod
    def constraint(self, q):
        pass

    @abc.abstractmethod
    def constraint_gradient(self, q):
        pass

    def constraint_velocity(self, q, p):
        return self.constraint_gradient(q) @ self.inverse_mass_matrix(q) @ p

    @abc.abstractmethod
    def dissipation_matrix(self, q, v):
        pass

    def rayleigh_dissipation(self, q, v):
        return 0.5 * v.T @ self.dissipation_matrix(q=q, v=v) @ v


class Pendulum3DCartesian(MultiBodySystem):

    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        nbr_constraints: int,
        nbr_dof: int,
        mass: float,
        gravity: list[float,],
        length: float,
    ):

        super().__init__(
            manager=manager,
            nbr_spatial_dimensions=nbr_spatial_dimensions,
            nbr_constraints=nbr_constraints,
            nbr_dof=nbr_dof,
            mass=mass,
            gravity=gravity,
        )

        self.length = length
        self.gravity = np.array(self.gravity)

    def get_momentum_from_velocity(
        self, position: list[float,], velocity: list[float,]
    ) -> list[float,]:
        momentum = self.mass_matrix() @ np.array(velocity)
        return momentum.tolist()

    def get_state_dimensions(self):
        return 2 * self.nbr_spatial_dimensions + self.nbr_constraints

    def get_state_columns(self):
        return [
            "x",
            "y",
            "z",
            "dx",
            "dy",
            "dz",
            "lambda",
        ]  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!

    def decompose_state(self):
        state = self.state
        dim = self.nbr_spatial_dimensions

        assert len(state) == 2 * dim + self.nbr_constraints

        decomposed_state = namedtuple(
            "decomposed_state", self.manager.integrator.variable_names
        )
        return decomposed_state(
            position=state[0:dim],
            momentum=state[dim : 2 * dim],
            multiplier=state[2 * dim :],
        )

    @staticmethod
    def compose_state(q, dq, lambd):
        return np.concatenate(
            [
                q,
                dq,
                lambd,
            ],
            axis=0,
        )

    def set_state(self, state):
        self.state = state

    def mass_matrix(self):
        return self.mass * np.eye(self.nbr_spatial_dimensions)

    def inverse_mass_matrix(self):
        return 1 / self.mass * np.eye(self.nbr_spatial_dimensions)

    def kinetic_energy_gradient_from_momentum(self):
        q = self.decompose_state().position
        return np.zeros(q.shape)

    def kinetic_energy_gradient_from_velocity(self):
        q = self.decompose_state().position
        return np.zeros(q.shape)

    def external_potential(self):
        q = self.decompose_state().position
        return -(self.mass_matrix() @ self.gravity).T @ q

    def external_potential_gradient(self):
        return -self.mass_matrix() @ self.gravity

    def internal_potential(self):
        return 0.0

    def internal_potential_gradient(self):
        q = self.decompose_state().position
        return np.zeros(q.shape)

    def constraint(self):
        q = self.decompose_state().position
        return np.array([0.5 * (q.T @ q / self.length**2 - 1.0)])

    def constraint_gradient(self):
        q = self.decompose_state().position
        return q.T[np.newaxis, :] / self.length**2

    def dissipation_matrix(self):
        q = self.decompose_state().position
        diss_mat = np.zeros(q.shape, q.shape)
        return diss_mat

    def angular_momentum(self):
        q = self.decompose_state().position
        p = self.decompose_state().momentum
        return np.cross(q, p)


class RigidBodyRotatingQuaternions(MultiBodySystem):
    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        nbr_constraints: int,
        nbr_dof: int,
        mass: float,
        gravity: list[float,],
        inertias: list[float,],
    ):

        super().__init__(
            manager=manager,
            nbr_spatial_dimensions=nbr_spatial_dimensions,
            nbr_constraints=nbr_constraints,
            nbr_dof=nbr_dof,
            mass=mass,
            gravity=gravity,
        )
        self.inertias = inertias
        self.inertias_matrix = np.diag(self.inertias)
        self.gravity = np.array(self.gravity)

    def get_momentum_from_velocity(
        self, position: list[float,], velocity: list[float,]
    ) -> list[float,]:
        momentum = self.mass_matrix(q=np.array(position)) @ np.array(velocity)
        return momentum.tolist()

    def get_state_dimensions(self):
        return 2 * self.nbr_dof + self.nbr_constraints

    def get_state_columns(self):
        return [
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
        ]  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!

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

    def mass_matrix(self, q):
        quat = q[0:4]
        G_q = operators.convective_transformation_matrix(
            quat=quat,
        )

        singular_mass_matrix = 4.0 * G_q.T @ self.inertias_matrix @ G_q
        regular_mass_matrix = singular_mass_matrix + 2 * np.trace(
            self.inertias_matrix
        ) * np.outer(quat, quat)

        return regular_mass_matrix

    def inverse_mass_matrix(self, q):
        quat = q[0:4]
        Ql_q = operators.left_multiplation_matrix(quat)
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

        Ql_p = operators.left_multiplation_matrix(p)

        return 0.25 * Ql_p @ inverse_extended_inertias @ Ql_p.T @ q

    def kinetic_energy_gradient_from_velocity(self, q, v):
        tmp = v[:4]

        G_v = operators.convective_transformation_matrix(
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

    def dissipation_matrix(self, q, v):
        diss_mat = np.zeros(q.shape, q.shape)
        return diss_mat


class FourParticleSystem(MultiBodySystem):

    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        nbr_constraints: int,
        nbr_dof: int,
        mass: list[float,],
        gravity: list[float,],
        rigid_constraint_length_12: float,
        rigid_constraint_length_34: float,
        natural_spring_length_13: float,
        natural_spring_length_24: float,
        spring_stiffness_parameter_13: float,
        spring_stiffness_parameter_24: float,
        damper_viscosity_parameter_23: float,
    ):

        super().__init__(
            manager=manager,
            nbr_spatial_dimensions=nbr_spatial_dimensions,
            nbr_constraints=nbr_constraints,
            nbr_dof=nbr_dof,
            mass=mass,
            gravity=gravity,
        )
        self.rigid_constraint_length_12 = rigid_constraint_length_12
        self.rigid_constraint_length_34 = rigid_constraint_length_34
        self.natural_spring_length_13 = natural_spring_length_13
        self.natural_spring_length_24 = natural_spring_length_24
        self.spring_stiffness_parameter_13 = spring_stiffness_parameter_13
        self.spring_stiffness_parameter_24 = spring_stiffness_parameter_24
        self.damper_viscosity_parameter_23 = damper_viscosity_parameter_23
        self.nbr_particles = 4

        self.gravity_vector = np.repeat(
            self.gravity,
            repeats=self.nbr_particles,
            axis=0,
        )

    def get_momentum_from_velocity(
        self, position: list[float,], velocity: list[float,]
    ) -> list[float,]:
        momentum = self.mass_matrix(q=None) @ np.array(velocity)
        return momentum.tolist()

    def get_state_dimensions(self):
        return (
            2 * self.nbr_spatial_dimensions * self.nbr_particles + self.nbr_constraints
        )

    def get_state_columns(self):
        return [
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
        ]  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!

    def decompose_state(self, state):
        dim = self.nbr_spatial_dimensions * self.nbr_particles

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

    def mass_matrix(self, q):
        diagonal_elements = np.repeat(self.mass, self.nbr_spatial_dimensions)
        return np.diag(diagonal_elements)

    def inverse_mass_matrix(self, q):
        diagonal_elements = np.reciprocal(
            np.repeat(self.mass, self.nbr_spatial_dimensions).astype(float)
        )
        return np.diag(diagonal_elements)

    def kinetic_energy_gradient_from_momentum(self, q, p):
        return np.zeros(q.shape)

    def kinetic_energy_gradient_from_velocity(self, q, v):
        return np.zeros(q.shape)

    def external_potential(self, q):
        return 0

    def external_potential_gradient(self, q):
        return np.zeros(q.shape)

    def internal_potential(self, q):
        q_1, q_2, q_3, q_4 = self.decompose_into_particles(q)

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
        q_1, q_2, q_3, q_4 = self.decompose_into_particles(q)

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
        q_1, q_2, q_3, q_4 = self.decompose_into_particles(q)
        first_constraint = 0.5 * (
            (q_2 - q_1).T @ (q_2 - q_1) - self.rigid_constraint_length_12**2
        )
        second_constraint = 0.5 * (
            (q_4 - q_3).T @ (q_4 - q_3) - self.rigid_constraint_length_34**2
        )

        return np.hstack([first_constraint, second_constraint])

    def constraint_gradient(self, q):
        q_1, q_2, q_3, q_4 = self.decompose_into_particles(q)

        first_constraint_gradient = np.hstack(
            [-(q_2 - q_1), (q_2 - q_1), np.zeros(3), np.zeros(3)]
        )
        second_constraint_gradient = np.hstack(
            [np.zeros(3), np.zeros(3), -(q_4 - q_3), (q_4 - q_3)]
        )
        return np.vstack([first_constraint_gradient, second_constraint_gradient])

    def decompose_into_particles(self, vector):

        assert len(vector) == self.nbr_particles * self.nbr_spatial_dimensions

        return np.split(vector, self.nbr_particles)

    def dissipation_matrix(self, q, v):
        diss_mat = np.zeros(q.shape, q.shape)
        return diss_mat


class ParticleSystem(MultiBodySystem):

    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        particles: list[dict,],
        springs: list[dict,],
        constraints: list[dict,],
        gravity: float,
    ):

        self.nbr_spatial_dimensions = nbr_spatial_dimensions
        self.particles = particles
        self.springs = springs
        self.constraints = constraints

        self.particles = utils.sort_list_of_dicts_based_on_special_value(
            my_list=self.particles,
            key="index",
        )
        self.nbr_particles = len(self.particles)
        nbr_dof = self.nbr_spatial_dimensions * self.nbr_particles

        mass = [particle["mass"] for particle in self.particles]

        self.initial_state_q = utils.get_flat_list_of_list_attributes(
            items=self.particles, key="initial_position"
        )

        self.initial_state_v = utils.get_flat_list_of_list_attributes(
            items=self.particles, key="initial_velocity"
        )

        super().__init__(
            manager=manager,
            nbr_spatial_dimensions=nbr_spatial_dimensions,
            nbr_constraints=len(self.constraints),
            nbr_dof=nbr_dof,
            mass=mass,
            gravity=gravity,
        )

        # TODO: Find a better solution (e.g. switching to Python indices), as this is a hacky fix of indices
        for attribute_name in ["springs", "dampers", "constraints"]:
            if hasattr(self, attribute_name):
                attribute = getattr(self, attribute_name)
                for entry in attribute:
                    for name in ["particle_start", "particle_end"]:
                        value = utils.shift_index_iterature_to_python(index=entry[name])
                        entry[name] = value
                setattr(self, attribute_name, attribute)

    def get_momentum_from_velocity(
        self, position: list[float,], velocity: list[float,]
    ) -> list[float,]:
        momentum = self.mass_matrix(q=None) @ np.array(velocity)
        return momentum.tolist()

    def get_state_dimensions(self):
        return 2 * self.nbr_dof + self.nbr_constraints

    def get_state_columns(self):
        return [
            f"{prefix}{letter}{utils.shift_index_python_to_literature(number)}"
            for prefix in ["", "d"]
            for number in range(self.nbr_particles)
            for letter in ["x", "y", "z"]
        ] + [
            f"lambda{utils.shift_index_python_to_literature(number)}"
            for number in range(self.nbr_constraints)
        ]  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!

    def decompose_state(self, state):

        assert len(state) == 2 * self.nbr_dof + self.nbr_constraints

        decomposed_state = namedtuple("state", "q p lambd")
        dim = self.nbr_dof

        return decomposed_state(
            q=state[0:dim],
            p=state[self.nbr_dof : 2 * dim],
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

    def mass_matrix(self, q):
        diagonal_elements = np.repeat(self.mass, self.nbr_spatial_dimensions)
        return np.diag(diagonal_elements)

    def inverse_mass_matrix(self, q):
        diagonal_elements = np.reciprocal(
            np.repeat(self.mass, self.nbr_spatial_dimensions).astype(float)
        )
        return np.diag(diagonal_elements)

    def kinetic_energy_gradient_from_momentum(self, q, p):
        return np.zeros(q.shape)

    def kinetic_energy_gradient_from_velocity(self, q, v):
        return np.zeros(q.shape)

    def external_potential(self, q):
        return 0

    def external_potential_gradient(self, q):
        return np.zeros(q.shape)

    @staticmethod
    def _spring_energy(stiffness, equilibrium_length, start, end):
        import scipy.linalg as linalg

        vector = end - start
        current_length = linalg.norm(vector)
        # return 0.5 * stiffness * (vector.T @ vector - equilibrium_length**2) ** 2  # This fits PLK solution but is wrong
        return 0.5 * stiffness * ((current_length - equilibrium_length)) ** 2

    def internal_potential(self, q):
        position_vectors = self.decompose_into_particles(q)

        contributions = [
            self._spring_energy(
                stiffness=spring["stiffness"],
                equilibrium_length=spring["equilibrium_length"],
                start=position_vectors[spring["particle_start"]],
                end=position_vectors[spring["particle_end"]],
            )
            for spring in self.springs
        ]

        return sum(contributions)

    @staticmethod
    def _spring_energy_gradient(
        stiffness,
        equilibrium_length,
        start_vector,
        end_vector,
        start_index,
        end_index,
        nbr_particles,
    ):
        vector = end_vector - start_vector
        tmp = (vector).T @ (vector) - equilibrium_length**2

        structure = []
        for index in range(nbr_particles):
            if index == start_index:
                structure.append(-2 * vector)
            elif index == end_index:
                structure.append(2 * vector)
            else:
                structure.append(np.zeros(3))

        return stiffness * tmp * np.hstack(structure)

    def internal_potential_gradient(self, q):
        position_vectors = self.decompose_into_particles(q)
        contributions = [
            self._spring_energy_gradient(
                stiffness=spring["stiffness"],
                equilibrium_length=spring["equilibrium_length"],
                start_vector=position_vectors[spring["particle_start"]],
                end_vector=position_vectors[spring["particle_end"]],
                start_index=spring["particle_start"],
                end_index=spring["particle_end"],
                nbr_particles=self.nbr_particles,
            )
            for spring in self.springs
        ]

        return sum(contributions)

    @staticmethod
    def _constraint(length, start, end):
        vector = end - start
        return 0.5 * (
            vector.T @ vector - length**2
        )  # TODO: Define reusable functions for common operations and avoid redundancy

    def constraint(self, q):

        position_vectors = self.decompose_into_particles(q)
        return [
            self._constraint(
                length=constraint["length"],
                start=position_vectors[constraint["particle_start"]],
                end=position_vectors[constraint["particle_end"]],
            )
            for constraint in self.constraints
        ]

    @staticmethod
    def _constraint_gradient(
        start_vector,
        end_vector,
        start_index,
        end_index,
        nbr_particles,
    ):
        vector = end_vector - start_vector

        structure = []
        for index in range(nbr_particles):
            if index == start_index:
                structure.append(-vector)
            elif index == end_index:
                structure.append(vector)
            else:
                structure.append(np.zeros(3))

        return np.hstack(structure)

    def constraint_gradient(self, q):

        position_vectors = self.decompose_into_particles(q)

        contributions = [
            self._constraint_gradient(
                start_vector=position_vectors[constraint["particle_start"]],
                end_vector=position_vectors[constraint["particle_end"]],
                start_index=constraint["particle_start"],
                end_index=constraint["particle_end"],
                nbr_particles=self.nbr_particles,
            )
            for constraint in self.constraints
        ]

        return np.vstack(contributions)

    def decompose_into_particles(self, vector):

        assert len(vector) == self.nbr_particles * self.nbr_spatial_dimensions

        return np.split(vector, self.nbr_particles)

    def dissipation_matrix(self, q, v):
        diss_mat = np.zeros(q.shape, q.shape)
        return diss_mat


class AbstractPortHamiltonianSystem(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def compose_state(self):
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

    @abc.abstractmethod
    def output(self, state):
        pass


class PortHamiltonianSystem(AbstractPortHamiltonianSystem):
    def __init__(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def decompose_state(self):
        pass

    @abc.abstractmethod
    def compose_state(self):
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
        mass: float,
        gravity: float,
        length: float,
    ):

        super().__init__(manager)
        self.mass = 1.0
        self.gravity = 9.81
        self.length = 1.0

    def get_state_dimensions(self):
        return 2

    def get_state_columns(self):
        return [
            "angle",
            "velocity",
        ]  # TODO: As the integrator defines whether it is velocity or momentum, this definition should be moved to integrator? Yes!

    def decompose_state(self, state):
        decomposed_state = namedtuple("state", "q v")
        return decomposed_state(
            q=state[0],
            v=state[1],
        )

    def compose_state(self):
        pass

    def costates(self, state):
        q, v = self.decompose_state(state=state)
        return np.array([self.mass * self.gravity * self.length * np.sin(q), v])

    def hamiltonian(self, state):
        pass

    def hamiltonian_gradient(self, state):
        q, v = self.decompose_state(state=state)
        return np.diag([self.mass * self.gravity * self.length * np.cos(q), 1])

    def structure_matrix(self, state):
        return np.array([[0, 1], [-1, 0]])

    def descriptor_matrix(self, state):
        return np.diag([1, self.mass * self.length**2])

    def port_matrix(self, state):
        pass

    def input(self):
        pass

    def dissipation_matrix(self, state):
        pass


class PortHamiltonianMBS(PortHamiltonianSystem):

    def __init__(self, manager):
        super().__init__(manager)
        self.mbs = manager.system

    def initialize_states(self):

        return self.mbs.compose_state(
            q=np.array(self.mbs.initial_state["Q"]),
            p=np.array(self.mbs.initial_state["V"]),
            lambd=np.zeros(self.mbs.nbr_constraints),
        )

    def get_state_dimensions(self):
        return self.mbs.get_state_dimensions()

    def get_state_columns(self):
        return self.mbs.get_state_columns()

    def decompose_state(self, state):
        decomposed_MBS_state = self.mbs.decompose_state(state)
        decomposed_state = namedtuple("state", "q v lambd")
        return decomposed_state(
            q=decomposed_MBS_state.q,
            v=decomposed_MBS_state.p,
            lambd=decomposed_MBS_state.lambd,
        )
        pass

    def compose_state(self):
        utils.pydykitException("not implemented")
        pass

    def costates(self, state):
        decomposed_state = self.decompose_state(state)
        potential_forces = self.mbs.external_potential_gradient(
            decomposed_state.q
        ) + self.mbs.internal_potential_gradient(decomposed_state.q)

        return np.hstack([potential_forces, decomposed_state.v, decomposed_state.lambd])

    def hamiltonian_gradient(self, state):
        decomposed_state = self.decompose_state(state)

        return self.mbs.external_potential_gradient(
            decomposed_state.q
        ) + self.mbs.internal_potential_gradient(decomposed_state.q)

    def structure_matrix(self, state):
        decomposed_state = self.decompose_state(state)
        q = decomposed_state.q
        v = decomposed_state.v
        lambd = decomposed_state.lambd
        G = self.mbs.constraint_gradient(q)

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

    def descriptor_matrix(self, state):
        identity_mat = np.eye(self.mbs.nbr_dof)
        decomposed_state = self.decompose_state(state)
        mass_matrix = self.mbs.mass_matrix(decomposed_state.q)
        zeros_matrix = np.zeros((self.mbs.nbr_constraints, self.mbs.nbr_constraints))
        descriptor_matrix = block_diag(identity_mat, mass_matrix, zeros_matrix)

        return descriptor_matrix

    def hamiltonian(self, state):
        pass

    def port_matrix(self, state):
        pass

    def input(self):
        pass

    def dissipation_matrix(self, state):
        pass
