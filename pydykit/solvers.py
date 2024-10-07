import abc

from . import base_classes, function_solvers, utils


class SystemSolver(base_classes.Solver):

    def __init__(self, manager: base_classes.Manager):
        self.manager = manager


class Newton(SystemSolver):

    def __init__(
        self,
        function_solver_name: str,
        newton_epsilon: float,
        max_iterations: int,
        **kwargs,
    ):
        super().__init__(**kwargs)

        function_solver_constructor = getattr(
            function_solvers,
            function_solver_name,
        )

        self.function_solver = function_solver_constructor(
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

            # Calc next state
            tmp = self.function_solver.solve(
                func=self.manager.integrator.get_residuum,
                jacobian=self.manager.integrator.get_tangent,
                initial=manager.current_state,
            )

            # Store results
            result.times[step.index] = step.time
            result.results[step.index, :] = manager.current_state = tmp

            # Print
            utils.print_current_step(step)

        return result
