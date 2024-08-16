import abc
from collections import namedtuple
from functools import partial

import numpy as np

from . import utils


class PortHamiltoniaIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        pass


class Midpoint(PortHamiltoniaIntegrator):
    def calc_residuum_tangent(self):
        system = self.manager.system
        states = system.states

        state_n = states.state_n
        state_n1 = states.state_n1

        time_step_size = self.manager.time_stepper.current_step.increment

        e_n = system.get_descriptor_matrix(state_n)
        e_n1 = system.get_descriptor_matrix(state_n1)

        z_vector = system.get_costates(
            state=0.5 * (state_n + state_n1),
        )
        jacobian = 0.5 * system.get_hamiltonian_gradient(state=state_n1)

        j_matrix = system.get_structure_matrix()

        residuum = (
            e_n1 @ state_n1 - e_n @ state_n - time_step_size * j_matrix @ z_vector
        )
        tangent = e_n1 - time_step_size * j_matrix @ jacobian

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )


class EulerImplicit(PortHamiltoniaIntegrator):
    def calc_residuum_tangent(self):
        system = self.manager.system
        states = system.states

        state_n = states.state_n
        state_n1 = states.state_n1
        time_step_size = self.manager.time_stepper.current_step.increment

        e_n = system.get_descriptor_matrix(state_n)
        e_n1 = system.get_descriptor_matrix(state_n1)

        z_vector = system.get_costates(
            state=state_n1,
        )
        jacobian = 0.5 * system.get_hamiltonian_gradient(
            state=state_n1,
        )

        j_matrix = system.get_structure_matrix()

        residuum = (
            e_n1 @ state_n1 - e_n @ state_n - time_step_size * j_matrix @ z_vector
        )
        tangent = e_n1 - time_step_size * j_matrix @ jacobian

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )


class EulerExplicit(PortHamiltoniaIntegrator):
    def calc_residuum_tangent(self):
        system = self.manager.system
        states = system.states

        state_n = states.state_n
        state_n1 = states.state_n1
        time_step_size = self.manager.time_stepper.current_step.increment

        e_n = system.get_descriptor_matrix(state_n)
        e_n1 = system.get_descriptor_matrix(state_n1)

        z_vector = system.get_costates(
            state=state_n,
        )

        j_matrix = system.get_structure_matrix()

        residuum = (
            e_n1 @ state_n1 - e_n @ state_n - time_step_size * j_matrix @ z_vector
        )
        tangent = e_n1

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )


class MultiBodyIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        pass


class MPStd(MultiBodyIntegrator):

    @staticmethod
    def calc_residuum(system, time_stepper, state_n, state_n1):

        step_size = time_stepper.current_step.increment

        q_n, p_n, lambd_n = system.decompose_state(state=state_n)
        q_n1, p_n1, lambd_n1 = system.decompose_state(state=state_n1)
        q_n05, p_n05, lambd_n05 = system.decompose_state(
            state=0.5 * (state_n + state_n1)
        )

        try:
            inv_mass_matrix_n05 = system.get_inverse_mass_matrix(q=q_n05)
        except AttributeError:
            mass_matrix_n05 = system.get_mass_matrix(q=q_n05)
            inv_mass_matrix_n05 = np.linalg.inv(mass_matrix_n05)

        G_n05 = system.constraint_gradient(q=q_n05)

        g_n1 = system.constraint(q=q_n1)

        DV_int_n05 = system.internal_potential_gradient(q=q_n05)
        DV_ext_n05 = system.external_potential_gradient(q=q_n05)
        DTq_n05 = system.kinetic_energy_gradient_from_momentum(
            q=q_n05,
            p=p_n05,
        )

        residuum_p = (
            p_n1
            - p_n
            + step_size * (DV_int_n05 + DV_ext_n05)
            + step_size * DTq_n05
            + step_size * G_n05.T @ lambd_n05
        )

        residuum = np.concatenate(
            [
                q_n1 - q_n - step_size * inv_mass_matrix_n05 @ p_n05,
                residuum_p,
                g_n1,
            ],
            axis=0,
        )

        return residuum

    def calc_residuum_tangent(self):
        system = self.manager.system
        states = system.states

        state_n = states.state_n
        state_n1 = states.state_n1

        residuum = self.calc_residuum(
            system=system,
            time_stepper=self.manager.time_stepper,
            state_n=state_n.copy(),
            state_n1=state_n1.copy(),
        )

        tangent = utils.get_numerical_tangent(
            func=partial(  # Bind some arguments to values
                self.calc_residuum,
                system=system,
                time_stepper=self.manager.time_stepper,
            ),
            state_1=state_n.copy(),
            state_2=state_n1.copy(),
        )

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )
