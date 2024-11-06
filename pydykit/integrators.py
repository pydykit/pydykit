import numpy as np

from . import abstract_base_classes, operators, utils


class IntegratorCommon(abstract_base_classes.Integrator):

    def __init__(self, manager):
        self.manager = manager

    def get_tangent(self, state):
        # will be used if no analytical tangent has been implemented
        return utils.get_numerical_tangent(
            func=self.get_residuum,
            state=state.copy(),
        )


class MidpointPH(IntegratorCommon):

    parametrization = ["state"]

    def get_residuum(self, next_state):

        # state_n1 is the argument which changes in calling function solver, state_n is the current state of the system
        state_n = self.manager.system.state
        state_n1 = next_state

        time_step_size = self.manager.time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)
        system_n, system_n1, system_n05 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
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


class DiscreteGradientPHDAE(IntegratorCommon):

    parametrization = ["state"]

    def __init__(self, manager, increment_tolerance):
        super().__init__(manager)
        self.increment_tolerance = increment_tolerance

    def get_residuum(self, next_state):

        # state_n1 is the argument which changes in calling function solver, state_n is the current state of the system
        state_n = self.manager.system.state
        state_n1 = next_state

        time_step_size = self.manager.time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)
        system_n, system_n1, system_n05 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
            states=[
                state_n,
                state_n1,
                state_n05,
            ],
        )

        differential_state_n = system_n.get_differential_state()
        differential_state_n1 = system_n1.get_differential_state()

        e_n05 = system_n05.descriptor_matrix()
        E_11_n05 = system_n05.nonsingular_descriptor_matrix()
        j_matrix_n05 = system_n05.structure_matrix()

        DGH = operators.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="hamiltonian",
            jacobian_name="hamiltonian_differential_gradient",
            argument_n=differential_state_n,
            argument_n1=differential_state_n1,
            type="Gonzalez",
            increment_tolerance=self.increment_tolerance,
        )

        differential_costate = np.linalg.solve(E_11_n05.T, DGH)
        algebraic_costate_2 = system_n05.get_algebraic_costate()
        costate = np.concatenate([differential_costate, algebraic_costate_2], axis=0)

        residuum = (
            e_n05 @ (state_n1 - state_n) - time_step_size * j_matrix_n05 @ costate
        )

        return residuum


class MidpointMultibody(IntegratorCommon):

    parametrization = ["position", "momentum", "multiplier"]

    def get_residuum(self, next_state):

        # state_n1 is the argument which changes in calling function solver, state_n is the current state of the system
        state_n = self.manager.system.state
        state_n1 = next_state

        # read time step size
        step_size = self.manager.time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)

        system_n, system_n1, system_n05 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
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


class DiscreteGradientMultibody(IntegratorCommon):

    parametrization = ["position", "momentum", "multiplier"]

    def __init__(self, manager, increment_tolerance):
        super().__init__(manager)
        self.increment_tolerance = increment_tolerance

    def get_residuum(self, next_state):

        # state_n1 is the argument which changes in calling function solver, state_n is the current state of the system
        state_n = self.manager.system.state
        state_n1 = next_state

        # read time step size
        step_size = self.manager.time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)

        system_n, system_n1, system_n05 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
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
        g_n1 = system_n1.constraint()

        # state contributions
        p_n = system_n.decompose_state()["momentum"]
        p_n1 = system_n1.decompose_state()["momentum"]
        p_n05 = system_n05.decompose_state()["momentum"]
        q_n = system_n.decompose_state()["position"]
        q_n1 = system_n1.decompose_state()["position"]
        q_n05 = system_n05.decompose_state()["position"]
        lambd_n05 = system_n05.decompose_state()["multiplier"]

        # discrete gradients
        G_DG = operators.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="constraint",
            jacobian_name="constraint_gradient",
            argument_n=q_n,
            argument_n1=q_n1,
            type="Gonzalez",
            increment_tolerance=self.increment_tolerance,
        )

        DV_int = operators.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="internal_potential",
            jacobian_name="internal_potential_gradient",
            argument_n=q_n,
            argument_n1=q_n1,
            type="Gonzalez",
            increment_tolerance=self.increment_tolerance,
        )

        DV_ext = operators.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="external_potential",
            jacobian_name="external_potential_gradient",
            argument_n=q_n,
            argument_n1=q_n1,
            type="Gonzalez",
            increment_tolerance=self.increment_tolerance,
        )

        # residuum contributions
        residuum_p = (
            p_n1 - p_n + step_size * (DV_int + DV_ext) + step_size * G_DG.T @ lambd_n05
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


class MidpointDAE(IntegratorCommon):

    parametrization = ["state"]

    def get_residuum(self, next_state):
        # state_n1 is the argument which changes in calling function solver, state_n is the current state of the system
        state_n = self.manager.system.state
        state_n1 = next_state

        # read time step size
        step_size = self.manager.time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)

        system_n05, system_n1 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
            states=[state_n05, state_n1],
        )

        return (
            system_n05.descriptor_matrix() @ (state_n1 - state_n)
            - step_size * system_n05.right_hand_side()
        )

    def get_tangent(self, state):
        # state_n1 is the argument which changes in calling function solver, state_n is the current state of the system
        state_n = self.manager.system.state
        state_n1 = state

        # read time step size
        step_size = self.manager.time_stepper.current_step.increment

        # create midpoint state and all corresponding discrete-time systems
        state_n05 = 0.5 * (state_n + state_n1)

        system_n05, system_n1 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
            states=[state_n05, state_n1],
        )
        return system_n05.descriptor_matrix() - step_size * system_n05.jacobian() * 0.5
