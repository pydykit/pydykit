import numpy as np

from . import abstract_base_classes, discrete_gradients, utils


class IntegratorCommon(abstract_base_classes.Integrator):

    def __init__(self, manager):
        self.manager = manager

    def get_tangent(self, state):
        # will be used if no analytical tangent has been implemented
        return utils.get_numerical_tangent(
            func=self.get_residuum,
            state=state.copy(),
        )

    def postprocess(self, next_state):
        pass


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

        e_n05 = system_n05.descriptor_matrix()

        # z_vector_n05 = system_n05.costates()
        costate = self.get_discrete_costate(
            system_n=system_n, system_n1=system_n1, system_n05=system_n05
        )

        j_matrix_n05 = system_n05.structure_matrix()
        r_matrix_n05 = system_n05.dissipation_matrix()

        residuum = (
            e_n05 @ (state_n1 - state_n)
            - time_step_size * (j_matrix_n05 - r_matrix_n05) @ costate
        )

        return residuum

    def dissipated_work(self, current_state, next_state, current_step):

        time_step_size = current_step.increment
        state_midpoint = 0.5 * (current_state + next_state)

        system_n, system_n05, system_n1 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
            states=[current_state, state_midpoint, next_state],
        )

        r_matrix_n05 = system_n05.dissipation_matrix()
        costates = system_n05.costates()

        return time_step_size * np.dot(costates, r_matrix_n05 @ costates)

    def get_discrete_costate(self, system_n, system_n1, system_n05):

        E_11_n05 = system_n05.nonsingular_descriptor_matrix()
        DH_n05 = system_n05.hamiltonian_differential_gradient()

        differential_costate = np.linalg.solve(E_11_n05.T, DH_n05)
        algebraic_costate = system_n1.get_algebraic_costate()
        costate = np.concatenate([differential_costate, algebraic_costate], axis=0)

        return costate


class DiscreteGradientPHDAE(IntegratorCommon):

    parametrization = ["state"]

    def __init__(self, manager, increment_tolerance, discrete_gradient_type):
        super().__init__(manager)
        self.increment_tolerance = increment_tolerance
        self.discrete_gradient_type = discrete_gradient_type

    def get_residuum(self, next_state):

        time_step_size = self.manager.time_stepper.current_step.increment
        current_state = self.manager.system.state
        state_midpoint = 0.5 * (current_state + next_state)

        system_n, system_n05, system_n1 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
            states=[current_state, state_midpoint, next_state],
        )
        costate = self.get_discrete_costate(
            system_n=system_n, system_n1=system_n1, system_n05=system_n05
        )

        e_matrix_n05 = system_n05.descriptor_matrix()
        j_matrix_n05 = system_n05.structure_matrix()
        r_matrix_n05 = system_n05.dissipation_matrix()

        residuum = (
            e_matrix_n05 @ (next_state - current_state)
            - time_step_size * (j_matrix_n05 - r_matrix_n05) @ costate
        )

        return residuum

    def get_discrete_costate(self, system_n, system_n1, system_n05):

        differential_state_n = system_n.get_differential_state()
        differential_state_n1 = system_n1.get_differential_state()

        E_11_n05 = system_n05.nonsingular_descriptor_matrix()

        DGH = discrete_gradients.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="hamiltonian",
            jacobian_name="hamiltonian_differential_gradient",
            argument_n=differential_state_n,
            argument_n1=differential_state_n1,
            type=self.discrete_gradient_type,
            increment_tolerance=self.increment_tolerance,
            nbr_func_parts=system_n.nbr_hamiltonian_parts,
            func_parts_n=system_n.differential_state_composition,
            func_parts_n1=system_n1.differential_state_composition,
        )

        differential_costate = np.linalg.solve(E_11_n05.T, DGH)
        algebraic_costate = system_n1.get_algebraic_costate()
        costate = np.concatenate([differential_costate, algebraic_costate], axis=0)

        return costate

    def dissipated_work(self, current_state, next_state, current_step):

        time_step_size = current_step.increment
        state_midpoint = 0.5 * (current_state + next_state)

        system_n, system_n05, system_n1 = utils.get_system_copies_with_desired_states(
            system=self.manager.system,
            states=[current_state, state_midpoint, next_state],
        )

        r_matrix_n05 = system_n05.dissipation_matrix()

        costate = self.get_discrete_costate(
            system_n=system_n, system_n1=system_n1, system_n05=system_n05
        )

        return time_step_size * np.dot(costate, r_matrix_n05 @ costate)


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

        # dissipation matrix
        D_n05 = system_n05.dissipation_matrix()

        # state contributions
        p_n = system_n.decompose_state()["momentum"]
        p_n1 = system_n1.decompose_state()["momentum"]
        p_n05 = system_n05.decompose_state()["momentum"]
        q_n = system_n.decompose_state()["position"]
        q_n1 = system_n1.decompose_state()["position"]
        lambd_n05 = system_n05.decompose_state()["multiplier"]

        residuum_p = (
            p_n1
            - p_n
            + step_size * (DV_int_n05 + DV_ext_n05)
            + step_size * DTq_n05
            # + step_size * G_n05.T @ lambd_n05
            + step_size * D_n05 @ inv_mass_matrix_n05 @ p_n05
        )

        if self.manager.system.nbr_constraints == 0:
            # No constraints
            residuum = np.concatenate(
                [
                    q_n1 - q_n - step_size * inv_mass_matrix_n05 @ p_n05,
                    residuum_p,
                    # g_n1,
                ],
                axis=0,
            )
        else:
            residuum_p = residuum_p + step_size * G_n05.T @ lambd_n05

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

    def __init__(self, manager, increment_tolerance, discrete_gradient_type):
        super().__init__(manager)
        self.increment_tolerance = increment_tolerance
        self.discrete_gradient_type = discrete_gradient_type

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

        # dissipation matrix
        D_n05 = system_n05.dissipation_matrix()

        # state contributions
        p_n = system_n.decompose_state()["momentum"]
        p_n1 = system_n1.decompose_state()["momentum"]
        p_n05 = system_n05.decompose_state()["momentum"]
        q_n = system_n.decompose_state()["position"]
        q_n1 = system_n1.decompose_state()["position"]
        q_n05 = system_n05.decompose_state()["position"]
        lambd_n05 = system_n05.decompose_state()["multiplier"]

        # discrete gradients
        G_DG = discrete_gradients.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="constraint",
            jacobian_name="constraint_gradient",
            argument_n=q_n,
            argument_n1=q_n1,
            type=self.discrete_gradient_type,
            increment_tolerance=self.increment_tolerance,
        )

        DV_int = discrete_gradients.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="internal_potential",
            jacobian_name="internal_potential_gradient",
            argument_n=q_n,
            argument_n1=q_n1,
            type=self.discrete_gradient_type,
            increment_tolerance=self.increment_tolerance,
        )

        DV_ext = discrete_gradients.discrete_gradient(
            system_n=system_n,
            system_n1=system_n1,
            system_n05=system_n05,
            func_name="external_potential",
            jacobian_name="external_potential_gradient",
            argument_n=q_n,
            argument_n1=q_n1,
            type=self.discrete_gradient_type,
            increment_tolerance=self.increment_tolerance,
        )

        # residuum contributions
        residuum_p = (
            p_n1
            - p_n
            + step_size * (DV_int + DV_ext)
            + step_size * D_n05 @ inv_mass_matrix_n05 @ p_n05
        )

        if self.manager.system.nbr_constraints == 0:
            # No constraints
            residuum = np.concatenate(
                [
                    q_n1 - q_n - step_size * inv_mass_matrix_n05 @ p_n05,
                    residuum_p,
                    # g_n1,
                ],
                axis=0,
            )

        else:

            residuum_p += step_size * G_DG.T @ lambd_n05

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
