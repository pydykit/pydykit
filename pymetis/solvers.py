import abc

import numpy as np


class Solver(abc.ABC):

    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    @abc.abstractmethod
    def solve(self, state_initial):
        pass


class Newton(Solver):

    def solve(self):
        system = self.manager.system
        time_stepper = self.manager.time_stepper

        system.initialize()
        states = system.states

        # Initialze the time stepper
        steps = time_stepper.make_steps()

        # Write first time to state.
        # Note: Initial state of system is already logged as well.
        step = next(steps)
        states.time[step.index] = step.time

        # Do remaining steps, until stepper stopps
        for step in steps:

            # Update system for NEW time based on previous state
            states.state_n = states.state_n1
            states.state_n1 = self.newton_update(
                time_step=step,  # TODO: Discuss whether passing this value explicitly is beneficial, or whether the integrator should access, e.g., manager.time_stepper.current_step. Note: We probably have to distinguish between physical time of the system, defined by time_stepper and the numerical time, used within the solver's iterations, which might be best controlled by the solver itself... Or is the time_stepper ment to manage the numerical time?
            )

            # Store results
            states.time[step.index] = step.time
            states.state[step.index, :] = states.state_n1

            print(f"time={step.time}")

        return states

    def newton_update(self, time_step):
        states = self.manager.system.states

        residual_norm = 1e5
        index_iteration = 0
        while (residual_norm >= self.newton_epsilon) and (
            index_iteration < self.max_iterations
        ):
            index_iteration += 1
            residual, tangent_matrix = self.manager.integrator.calc_residuum_tangent(
                time_step=time_step,
            )
            state_delta = -np.linalg.inv(tangent_matrix) @ residual
            states.state_n1 = states.state_n1 + state_delta
            residual_norm = np.linalg.norm(residual)

        return states.state_n1
