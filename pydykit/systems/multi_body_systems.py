import abc
import copy

import numpy as np

from .. import base_classes, operators, utils


class MultiBodySystem(base_classes.AbstractMultiBodySystem):
    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        nbr_constraints: int,
        nbr_dof: int,
        mass: float,
        gravity: list[float,],
        state,
    ):
        self.manager = manager
        self.state = state
        self.nbr_spatial_dimensions = nbr_spatial_dimensions
        self.nbr_constraints = nbr_constraints
        self.nbr_dof = nbr_dof
        self.mass = mass
        self.gravity = gravity

        self.initialize_state(state)

    def initialize_state(self, state):

        # convert state as dict to array with values
        self.initial_state = state
        self.dim_state = utils.get_nbr_elements_dict_list(self.initial_state)
        self.state_names = utils.get_keys_dict_list(self.initial_state)

        # TODO: Improve attribute name "variable_names" as the current name indicates that the names are variable. It says nearly nothing.
        # TODO: Use "variable_names" for all integrators, if you think it is a good idea, otherwise remove this check.
        # TODO: Why do you test, whether integrator and system are compatible here within the function "initialize_state"? Shouldn't this be done somewhere else and separated from action?
        if hasattr(self.manager.integrator, "variable_names"):
            utils.compare_string_lists(
                list1=self.state_names,
                list2=self.manager.integrator.variable_names,
            )

        self.state_columns = self.get_state_columns()
        self.build_state_vector()

    def build_state_vector(self):
        self.state = np.hstack(list(self.initial_state.values()))

    def decompose_state(self):
        return dict(
            zip(
                self.state_names,
                [
                    self.state[0 : self.nbr_dof],
                    self.state[self.nbr_dof : 2 * self.nbr_dof],
                    self.state[2 * self.nbr_dof :],
                ],
            )
        )

    def get_state_columns(self):
        return [
            f"{state_name}{utils.shift_index_python_to_literature(number)}"
            for state_name in self.state_names[:2]
            for number in range(self.nbr_dof)
        ] + [
            f"lambda{utils.shift_index_python_to_literature(number)}"
            for number in range(self.nbr_constraints)
        ]

    def update(self, *states):
        # for each entry in states a system is created
        systems = []
        for state in states:
            self.state = state
            systems.append(copy.copy(self))
        return systems

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
        state,
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
            state=state,
            gravity=gravity,
        )

        self.length = length
        self.gravity = np.array(self.gravity)

    def mass_matrix(self):
        return self.mass * np.eye(self.nbr_dof)

    def inverse_mass_matrix(self):
        return 1 / self.mass * np.eye(self.nbr_dof)

    def kinetic_energy_gradient_from_momentum(self):
        q = self.decompose_state()["position"]
        return np.zeros(q.shape)

    def kinetic_energy_gradient_from_velocity(self):
        q = self.decompose_state()["position"]
        return np.zeros(q.shape)

    def external_potential(self):
        q = self.decompose_state()["position"]
        return -(self.mass_matrix() @ self.gravity).T @ q

    def external_potential_gradient(self):
        return -self.mass_matrix() @ self.gravity

    def internal_potential(self):
        return 0.0

    def internal_potential_gradient(self):
        q = self.decompose_state()["position"]
        return np.zeros(q.shape)

    def constraint(self):
        q = self.decompose_state()["position"]
        return np.array([0.5 * (q.T @ q / self.length**2 - 1.0)])

    def constraint_gradient(self):
        q = self.decompose_state()["position"]
        return q.T[np.newaxis, :] / self.length**2

    def dissipation_matrix(self):
        q = self.decompose_state()["position"]
        diss_mat = np.zeros(q.shape, q.shape)
        return diss_mat

    def angular_momentum(self):
        q = self.decompose_state()["position"]
        p = self.decompose_state()["momentum"]
        return np.cross(q, p)


class RigidBodyRotatingQuaternions(MultiBodySystem):
    def __init__(
        self,
        manager,
        state,
        nbr_spatial_dimensions: int,
        nbr_constraints: int,
        nbr_dof: int,
        mass: float,
        gravity: list[float,],
        inertias: list[float,],
    ):
        self.inertias = inertias
        self.inertias_matrix = np.diag(self.inertias)

        super().__init__(
            manager=manager,
            state=state,
            nbr_spatial_dimensions=nbr_spatial_dimensions,
            nbr_constraints=nbr_constraints,
            nbr_dof=nbr_dof,
            mass=mass,
            gravity=gravity,
        )
        self.gravity = np.array(self.gravity)

    def mass_matrix(self):
        q = self.decompose_state()["position"]
        quat = q[0:4]
        G_q = operators.convective_transformation_matrix(
            quat=quat,
        )
        singular_mass_matrix = 4.0 * G_q.T @ self.inertias_matrix @ G_q
        regular_mass_matrix = singular_mass_matrix + 2 * np.trace(
            self.inertias_matrix
        ) * np.outer(quat, quat)

        return regular_mass_matrix

    def inverse_mass_matrix(self):
        q = self.decompose_state()["position"]
        quat = q[0:4]
        Ql_q = operators.left_multiplation_matrix(quat)
        J0 = 0.5 * np.trace(self.inertias_matrix)
        inverse_inertias = 1.0 / np.diag(self.inertias_matrix)
        inverse_extended_inertias_matrix = np.diag(np.append(1 / J0, inverse_inertias))

        return 0.25 * Ql_q @ inverse_extended_inertias_matrix @ Ql_q.T

    def kinetic_energy_gradient_from_momentum(self):
        q = self.decompose_state()["position"]
        p = self.decompose_state()["momentum"]

        # extended inertia tensor
        J0 = np.trace(self.inertias_matrix)
        extended_inertias = np.block(
            [[J0, np.zeros((1, 3))], [np.zeros((3, 1)), self.inertias_matrix]]
        )

        inverse_extended_inertias = np.linalg.inv(extended_inertias)

        Ql_p = operators.left_multiplation_matrix(p)

        return 0.25 * Ql_p @ inverse_extended_inertias @ Ql_p.T @ q

    def kinetic_energy_gradient_from_velocity(self):
        q = self.decompose_state()["position"]
        v = self.decompose_state()["velocity"]

        tmp = v[:4]

        G_v = operators.convective_transformation_matrix(
            quat=tmp,
        )
        M_4_hat = operators.combine_G_inertias(
            g_matrix=G_v,
            inertias=self.inertias_matrix,
        )

        return M_4_hat @ q

    def external_potential(self):
        return 0.0

    def external_potential_gradient(self):
        q = self.decompose_state()["position"]
        return np.zeros(q.shape)

    def internal_potential(self):
        return 0.0

    def internal_potential_gradient(self):
        q = self.decompose_state()["position"]
        return np.zeros(q.shape)

    def constraint(self):
        q = self.decompose_state()["position"]
        return np.array([0.5 * (q.T @ q - 1.0)])

    def constraint_gradient(self):
        q = self.decompose_state()["position"]
        return q.T[np.newaxis, :]

    def dissipation_matrix(self):
        q = self.decompose_state()["position"]
        v = self.decompose_state()["velocity"]

        diss_mat = np.zeros(q.shape, v.shape)
        return diss_mat


class FourParticleSystem(MultiBodySystem):

    def __init__(
        self,
        manager,
        state,
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
            state=state,
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

    def mass_matrix(self):
        diagonal_elements = np.repeat(self.mass, self.nbr_spatial_dimensions)
        return np.diag(diagonal_elements)

    def inverse_mass_matrix(self):
        diagonal_elements = np.reciprocal(
            np.repeat(self.mass, self.nbr_spatial_dimensions).astype(float)
        )
        return np.diag(diagonal_elements)

    def kinetic_energy_gradient_from_momentum(self):
        return np.zeros(self.nbr_dof)

    def kinetic_energy_gradient_from_velocity(self):
        return np.zeros(self.nbr_dof)

    def external_potential(self):
        return 0

    def external_potential_gradient(self):
        return np.zeros(self.nbr_dof)

    def internal_potential(self):
        q = self.decompose_state()["position"]
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

    def internal_potential_gradient(self):
        q = self.decompose_state()["position"]
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

    def constraint(self):
        q = self.decompose_state()["position"]
        q_1, q_2, q_3, q_4 = self.decompose_into_particles(q)
        first_constraint = 0.5 * (
            (q_2 - q_1).T @ (q_2 - q_1) - self.rigid_constraint_length_12**2
        )
        second_constraint = 0.5 * (
            (q_4 - q_3).T @ (q_4 - q_3) - self.rigid_constraint_length_34**2
        )

        return np.hstack([first_constraint, second_constraint])

    def constraint_gradient(self):
        q = self.decompose_state()["position"]
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

    def dissipation_matrix(self):
        diss_mat = np.zeros(self.nbr_dof, self.nbr_dof)
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

        self.initial_state_p = utils.get_flat_list_of_list_attributes(
            items=self.particles, key="initial_momentum"
        )
        self.initial_state = {
            "position": self.initial_state_q,
            "momentum": self.initial_state_p,
            "multiplier": np.zeros(len(self.constraints)),
        }

        super().__init__(
            manager=manager,
            nbr_spatial_dimensions=nbr_spatial_dimensions,
            nbr_constraints=len(self.constraints),
            nbr_dof=nbr_dof,
            mass=mass,
            gravity=gravity,
            state=self.initial_state,
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

    def get_state_columns(self):
        return [
            f"{state_name}_{letter}{utils.shift_index_python_to_literature(number)}"
            for state_name in self.state_names[:2]
            for number in range(self.nbr_particles)
            for letter in ["x", "y", "z"]
        ] + [
            f"lambda{utils.shift_index_python_to_literature(number)}"
            for number in range(self.nbr_constraints)
        ]

    def mass_matrix(self):
        diagonal_elements = np.repeat(self.mass, self.nbr_spatial_dimensions)
        return np.diag(diagonal_elements)

    def inverse_mass_matrix(self):
        diagonal_elements = np.reciprocal(
            np.repeat(self.mass, self.nbr_spatial_dimensions).astype(float)
        )
        return np.diag(diagonal_elements)

    def kinetic_energy_gradient_from_momentum(self):
        return np.zeros(self.nbr_dof)

    def kinetic_energy_gradient_from_velocity(self):
        return np.zeros(self.nbr_dof)

    def external_potential(self):
        return 0

    def external_potential_gradient(self):
        return np.zeros(self.nbr_dof)

    @staticmethod
    def _spring_energy(stiffness, equilibrium_length, start, end):
        import scipy.linalg as linalg

        vector = end - start
        current_length = linalg.norm(vector)
        # return 0.5 * stiffness * (vector.T @ vector - equilibrium_length**2) ** 2  # This fits PLK solution but is wrong
        return 0.5 * stiffness * ((current_length - equilibrium_length)) ** 2

    def internal_potential(self):
        q = self.decompose_state()["position"]
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

    def internal_potential_gradient(self):
        q = self.decompose_state()["position"]
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

    def constraint(self):
        q = self.decompose_state()["position"]
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

    def constraint_gradient(self):
        q = self.decompose_state()["position"]
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

    def dissipation_matrix(self):
        diss_mat = np.zeros(self.nbr_dof, self.nbr_dof)
        return diss_mat
