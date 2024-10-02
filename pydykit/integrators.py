import abc
import copy
from collections import namedtuple
from functools import partial

import numpy as np

from . import utils


class PortHamiltonianIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        pass


class MidpointPH(PortHamiltonianIntegrator):
    def __init__(self, manager):
        super().__init__(manager)
        self.variable_names = ["position", "velocity", "multiplier"]

    def calc_residuum_tangent(self):
        system = self.manager.system
        manager = self.manager

        current_state = manager.current_state
        next_state = manager.next_state

        residuum = self.calc_residuum(
            system=system,
            time_stepper=self.manager.time_stepper,
            state_n=current_state.copy(),
            state_n1=next_state.copy(),
        )

        tangent = utils.get_numerical_tangent(
            func=partial(  # Bind some arguments to values
                self.calc_residuum,
                system=system,
                time_stepper=self.manager.time_stepper,
            ),
            state_1=current_state.copy(),
            state_2=next_state.copy(),
        )

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )

    @staticmethod
    def calc_residuum(system, time_stepper, state_n, state_n1):

        time_step_size = time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)
        system_n, system_n1, system_n05 = system.update(state_n, state_n1, state_n05)

        e_n = system_n.descriptor_matrix()
        e_n1 = system_n1.descriptor_matrix()

        z_vector_n05 = system_n05.costates()

        j_matrix_n05 = system_n05.structure_matrix()

        residuum = (
            e_n1 @ state_n1
            - e_n @ state_n
            - time_step_size * j_matrix_n05 @ z_vector_n05
        )

        return residuum


class MultiBodyIntegrator(abc.ABC):
    integrator_output = namedtuple("integrator_output", "residuum tangent")

    def __init__(self, manager):
        self.manager = manager

    @abc.abstractmethod
    def calc_residuum_tangent(self):
        pass


class Midpoint_DAE(MultiBodyIntegrator):

    def __init__(self, manager):
        super().__init__(manager)
        self.variable_names = ["position", "momentum", "multiplier"]

    @staticmethod
    def calc_residuum(system, time_stepper, state_n, state_n1):

        # read time step size
        step_size = time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)
        system_n, system_n1, system_n05 = system.update(state_n, state_n1, state_n05)

        # get inverse mass matrix
        try:
            inv_mass_matrix_n05 = system_n05.inverse_mass_matrix()
        except AttributeError:
            mass_matrix_n05 = system_n05.mass_matrix()
            inv_mass_matrix_n05 = np.linalg.inv(mass_matrix_n05)

        # constraint
        G_n05 = system_n05.constraint_gradient()
        g_n1 = system_n1.constraint()

        # energetic gradients
        DV_int_n05 = system_n05.internal_potential_gradient()
        DV_ext_n05 = system_n05.external_potential_gradient()
        DTq_n05 = system_n05.kinetic_energy_gradient_from_momentum()

        # state contributions
        p_n = system_n.decompose_state()["momentum"]
        p_n1 = system_n1.decompose_state()["momentum"]
        p_n05 = system_n05.decompose_state()["momentum"]
        q_n = system_n.decompose_state()["position"]
        q_n1 = system_n1.decompose_state()["position"]
        lambd_n05 = system_n05.decompose_state()["multiplier"]

        # residuum contributions
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
        manager = self.manager

        current_state = manager.current_state
        next_state = manager.next_state

        residuum = self.calc_residuum(
            system=system,
            time_stepper=self.manager.time_stepper,
            state_n=current_state.copy(),
            state_n1=next_state.copy(),
        )

        tangent = utils.get_numerical_tangent(
            func=partial(  # Bind some arguments to values
                self.calc_residuum,
                system=system,
                time_stepper=self.manager.time_stepper,
            ),
            state_1=current_state.copy(),
            state_2=next_state.copy(),
        )

        return self.integrator_output(
            residuum=residuum,
            tangent=tangent,
        )
