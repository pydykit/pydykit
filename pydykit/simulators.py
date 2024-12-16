from . import abstract_base_classes, solvers, utils


class Simulator(abstract_base_classes.Simulator):

    def __init__(self, manager: abstract_base_classes.Manager):
        self.manager = manager


class OneStep(Simulator):

    def __init__(
        self,
        solver_name: str,
        newton_epsilon: float,
        max_iterations: int,
        **kwargs,
    ):
        super().__init__(**kwargs)

        solver_constructor = getattr(
            solvers,
            solver_name,
        )

        self.solver = solver_constructor(
            newton_epsilon=newton_epsilon,
            max_iterations=max_iterations,
        )

    def run(self, result):
        time_stepper = self.manager.time_stepper
        manager = self.manager
        manager.validate_integrator_system_combination()

        # Initialze the time stepper
        steps = time_stepper.make_steps()
        step = next(steps)

        # First step
        result.times[step.index] = step.time
        utils.print_current_step(step)

        # Do remaining steps, until stepper stops
        for step in steps:

            if not self.solver.has_failed:
                # Calc next state
                next_state = self.solver.solve(
                    func=manager.integrator.get_residuum,
                    jacobian=manager.integrator.get_tangent,
                    initial=manager.system.state,
                )

                # Store results
                result.times[step.index] = step.time
                result.results[step.index, :] = manager.system.state = next_state

                # Print
                utils.print_current_step(step)

            else:
                return result

        return result
