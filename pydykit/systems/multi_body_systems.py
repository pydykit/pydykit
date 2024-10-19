import numpy as np

from .. import abstract_base_classes, operators, utils
from .system import System


class MultiBodySystem(
    abstract_base_classes.AbstractMultiBodySystem,
    System,  # TODO: Avoid multi-inheritance if possible
):
    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        nbr_constraints: int,
        nbr_dof: int,
        mass: float,
        gravity: list[float,],
        state: dict[str, list[float]],
    ):
        self.manager = manager

        self.nbr_spatial_dimensions = nbr_spatial_dimensions
        self.nbr_constraints = nbr_constraints
        self.nbr_dof = nbr_dof
        self.mass = mass
        self.gravity = gravity
        self.initialize_state(state)
        self.assert_used_integrator()

    def initialize_state(self, state):

        # convert state as dict to array with values
        self.initial_state = state
        self.dim_state = utils.get_nbr_elements_dict_list(self.initial_state)
        self.state_names = utils.get_keys_dict_list(self.initial_state)
        self.state_columns = self.get_state_columns()
        self.build_state_vector()

    def assert_used_integrator(self):
        if hasattr(self.manager.integrator, "names_of_used_variables"):
            utils.compare_string_lists(
                list1=self.state_names,
                list2=self.manager.integrator.names_of_used_variables,
            )

    def get_state_columns(self):
        return [
            f"{state_name}{number+1}"
            for state_name in ["position", "momentum"]
            for number in range(self.nbr_dof)
        ] + [f"lambda{number+1}" for number in range(self.nbr_constraints)]

    def build_state_vector(self):
        self.state = np.hstack(
            list(self.initial_state.values())
        )  # BUG: You set .state here again

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

    def kinetic_energy(self):
        q = self.state.decompose_state()["position"]
        p = self.state.decompose_state()["momentum"]
        return 0.5 * p.T @ self.inverse_mass_matrix(q=q) @ p

    def potential_energy(self):
        return self.external_potential() + self.internal_potential()

    def potential_energy_gradient(self):
        return self.external_potential_gradient() + self.internal_potential_gradient()

    def total_energy(self):
        return self.kinetic_energy() + self.potential_energy()

    def constraint_velocity(self):
        p = self.decompose_state()["momentum"]
        return self.constraint_gradient() @ self.inverse_mass_matrix() @ p

    def rayleigh_dissipation(self):
        v = self.decompose_state()["velocity"]
        return 0.5 * v.T @ self.dissipation_matrix() @ v


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
        return np.array([utils.quadratic_length_constraint(vector=q, length=1.0)])

    def constraint_gradient(self):
        q = self.decompose_state()["position"]
        return q.T[np.newaxis, :]

    def dissipation_matrix(self):
        q = self.decompose_state()["position"]
        v = self.decompose_state()["velocity"]

        diss_mat = np.zeros(q.shape, v.shape)
        return diss_mat


class ParticleSystem(MultiBodySystem):

    def __init__(
        self,
        manager,
        nbr_spatial_dimensions: int,
        particles: list[dict,],
        springs: list[dict,],
        constraints: list[dict,],
        supports: list[dict,],
        gravity: float,
    ):

        self.nbr_spatial_dimensions = nbr_spatial_dimensions
        self.particles = utils.sort_list_of_dicts_based_on_special_value(
            my_list=particles,
            key="index",
        )
        self.springs = springs
        self.constraints = constraints
        self.supports = utils.sort_list_of_dicts_based_on_special_value(
            my_list=supports, key="index"
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

        # TODO: Remove redundancy... You pass several arguments to a super class and set them as attributes within the super classes init function.
        # Some of these arguments have already been set as attributes within this childs init function. Why would you do this?
        # TODO: Remove everything that has to do with parsing config files from system. System is about methods which evaluate physical quantities.
        super().__init__(
            manager=manager,
            nbr_spatial_dimensions=nbr_spatial_dimensions,
            nbr_constraints=len(self.constraints),
            nbr_dof=nbr_dof,
            mass=mass,
            gravity=gravity,
            state=self.initial_state,
        )

    def get_state_columns(self):
        return [
            f"{state_name}_{letter}{number+1}"
            for state_name in ["position", "momentum"]
            for number in range(self.nbr_particles)
            for letter in ["x", "y", "z"]
        ] + [f"lambda{number+1}" for number in range(self.nbr_constraints)]

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
        q = self.decompose_state()["position"]
        body_force = self._body_force()
        return body_force.T @ q

    def external_potential_gradient(self):

        return self._body_force()

    def _body_force(self):
        single_particle_gravity = np.zeros(self.nbr_spatial_dimensions)
        single_particle_gravity[-1] = self.gravity
        body_force = self.mass_matrix() @ np.repeat(
            single_particle_gravity, self.nbr_particles
        )
        return body_force

    @staticmethod
    def _spring_energy(stiffness, equilibrium_length, start, end):
        vector = end - start
        return 0.5 * stiffness * (vector.T @ vector - equilibrium_length**2) ** 2

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
        return utils.quadratic_length_constraint(vector=vector, length=length)

    def constraint(self):
        q = self.decompose_state()["position"]
        position_vectors = dict(
            particle=self.decompose_into_particles(q),
            support=self.get_positions_supports(),
        )

        return [
            self._constraint(
                length=constraint["length"],
                start=utils.select(
                    position_vectors=position_vectors,
                    constraint=constraint,
                    endpoint="start",
                ),
                end=utils.select(
                    position_vectors=position_vectors,
                    constraint=constraint,
                    endpoint="end",
                ),
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
        position_vectors = dict(
            particle=self.decompose_into_particles(q),
            support=self.get_positions_supports(),
        )

        contributions = [
            self._constraint_gradient(
                start_vector=utils.select(
                    position_vectors=position_vectors,
                    constraint=constraint,
                    endpoint="start",
                ),
                end_vector=utils.select(
                    position_vectors=position_vectors,
                    constraint=constraint,
                    endpoint="end",
                ),
                start_index=(
                    constraint["start"]["index"]
                    if constraint["start"]["type"] == "particle"
                    else None
                ),
                end_index=(
                    constraint["end"]["index"]
                    if constraint["end"]["type"] == "particle"
                    else None
                ),
                nbr_particles=self.nbr_particles,
            )
            for constraint in self.constraints
        ]

        return np.vstack(contributions)

    def decompose_into_particles(self, vector):

        assert len(vector) == self.nbr_particles * self.nbr_spatial_dimensions

        return np.split(vector, self.nbr_particles)

    def get_positions_supports(self):
        return [np.array(support["position"]) for support in self.supports]

    def dissipation_matrix(self):
        diss_mat = np.zeros(self.nbr_dof, self.nbr_dof)
        return diss_mat
