import numpy as np

from . import base_classes, utils


class Newton(base_classes.Solver):

    def solve(self):
        time_stepper = self.manager.time_stepper
        manager = self.manager
        result = manager.result

        # Initialze the time stepper
        steps = time_stepper.make_steps()
        step = next(steps)

        # First step
        result.times[step.index] = step.time
        utils.print_current_step(step)

        # Do remaining steps, until stepper stops
        for step in steps:

            # Update system for NEW time based on previous state
            manager.current_state = manager.next_state
            manager.next_state = (
                self.newton_update()  # Note: current time step size can be access through time_stepper.current_step.increment
            )

            # Store results
            result.times[step.index] = step.time
            result.results[step.index, :] = manager.next_state

            # Print
            utils.print_current_step(step)

        return result

    def newton_update(self):
        manager = self.manager

        # Newton iteration starts
        residual_norm = 1e5
        index_iteration = 0

        # Iterate while residual isnt zero and max. iterations number isnt reached
        while (residual_norm >= self.newton_epsilon) and (
            index_iteration < self.max_iterations
        ):
            index_iteration += 1
            residual, tangent_matrix = self.manager.integrator.calc_residuum_tangent()
            state_delta = -np.linalg.inv(tangent_matrix) @ residual
            manager.next_state = manager.next_state + state_delta
            residual_norm = np.linalg.norm(residual)
            utils.print_residual_norm(value=residual_norm)

        if residual_norm < self.newton_epsilon:
            pass
        else:
            raise utils.PydykitException(
                f"Newton convergence not succesful in step with index {self.manager.time_stepper.current_step.index}."
            )

        return manager.next_state
