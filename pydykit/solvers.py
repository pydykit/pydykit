import abc

import numpy as np

from . import utils


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

        if not self.manager.called_from_test:
            utils.print_current_step(step)
        else:
            pass

        # Do remaining steps, until stepper stopps
        for step in steps:

            # Update system for NEW time based on previous state
            states.state_n = states.state_n1
            states.state_n1 = (
                self.newton_update()  # Note: current time step size can be access through time_stepper.current_step.increment
            )

            # Store results
            states.time[step.index] = step.time
            states.state[step.index, :] = states.state_n1

            utils.print_current_step(step)

        return states

    def newton_update(self):
        states = self.manager.system.states

        residual_norm = 1e5
        index_iteration = 0
        while (residual_norm >= self.newton_epsilon) and (
            index_iteration < self.max_iterations
        ):
            index_iteration += 1
            residual, tangent_matrix = self.manager.integrator.calc_residuum_tangent()
            state_delta = -np.linalg.inv(tangent_matrix) @ residual
            states.state_n1 = states.state_n1 + state_delta
            residual_norm = np.linalg.norm(residual)

            utils.print_residual_norm(value=residual_norm)

        if residual_norm < self.newton_epsilon:
            pass
        else:
            raise utils.PydykitException(
                f"Newton convergence not succesful in step with index {self.manager.time_stepper.current_step.index}."
            )

        return states.state_n1
