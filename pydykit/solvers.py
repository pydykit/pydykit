import abc

from . import base_classes, function_solvers, utils


class SystemSolver(abc.ABC):

    def __init__(self, manager: base_classes.Manager):
        self.manager = manager

    @abc.abstractmethod
    def solve(self):
        raise NotImplementedError


class Newton(SystemSolver):

    def __init__(
        self,
        newton_epsilon: float,
        max_iterations: int,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.function_solver = function_solvers.Newton(
            newton_epsilon=newton_epsilon,
            max_iterations=max_iterations,
        )

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
            manager.next_state = self.function_solver.solve(
                func=self.manager.integrator.get_residuum,
                jacobian=self.manager.integrator.get_tangent,
                initial=manager.next_state,
            )

            # Store results
            result.times[step.index] = step.time
            result.results[step.index, :] = manager.next_state

            # Print
            utils.print_current_step(step)

        return result
