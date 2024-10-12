from functools import partial

import numpy as np

from . import abstract_base_classes, utils


class IntegratorCommon(abstract_base_classes.Integrator):

    def __init__(self, manager):
        self.manager = manager

    # TODO: Simplify the life of "state".
    # Why don't we just have a system, which state is defined by its attribute
    # "state" and that's it?
    # Why should the manager keep current_state and next_state?
    # A system does have one state, that's it.
    # The next state of the system is calculated on the fly by the solver
    # which could be external and therefore would not like to change
    # the states of any manager or even system.
    # If the next state is calculated, than we increment our systems state
    # and log the old one on the result object.

    def get_residuum(self, state):
        # TODO: This is silly, improve it
        return self.calc_residuum(
            system=self.manager.system,
            time_stepper=self.manager.time_stepper,
            state_n=self.manager.system.state.copy(),
            state_n1=state.copy(),
        )

    def get_tangent(self, state):
        # TODO: This is silly, improve it
        return utils.get_numerical_tangent(
            func=partial(  # Bind some arguments to values
                self.calc_residuum,
                system=self.manager.system,
                time_stepper=self.manager.time_stepper,
            ),
            state_1=self.manager.system.state.copy(),
            state_2=state.copy(),
        )


class MidpointPH(IntegratorCommon):

    @staticmethod
    def calc_residuum(system, time_stepper, state_n, state_n1):

        time_step_size = time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)
        system_n, system_n1, system_n05 = utils.get_system_copies_with_desired_states(
            system=system,
            states=[
                state_n,
                state_n1,
                state_n05,
            ],
        )

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


class Midpoint_DAE(IntegratorCommon):

    variable_names = ["position", "momentum", "multiplier"]

    @staticmethod
    def calc_residuum(system, time_stepper, state_n, state_n1):

        # read time step size
        step_size = time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)

        system_n, system_n1, system_n05 = utils.get_system_copies_with_desired_states(
            system=system,
            states=[
                state_n,
                state_n1,
                state_n05,
            ],
        )

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
