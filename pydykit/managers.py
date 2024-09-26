import copy

from . import configuration, integrators, solvers, systems, time_steppers


class Manager:

    def configure(
        self,
        configuration: configuration.Configuration,
    ):

        self.configuration = configuration

        self.system = self._set_system()
        self.solver = self._set_solver()
        self.integrator = self._set_integrator()
        self.time_stepper = self._set_time_stepper()

    def _set_system(
        self,
    ) -> (
        systems.FourParticleSystem
        | systems.MultiBodySystem
        | systems.ParticleSystem
        | systems.Pendulum2D
        | systems.Pendulum3DCartesian
    ):

        return self._dynamically_instantiate(
            module=systems,
            class_name=self.configuration.system.class_name,
            kwargs=self.configuration.system.kwargs,
        )

    def _set_solver(self) -> solvers.Solver | solvers.Newton:

        return self._dynamically_instantiate(
            module=solvers,
            class_name=self.configuration.solver.class_name,
            kwargs=self.configuration.solver.kwargs,
        )

    def _set_integrator(
        self,
    ) -> (
        integrators.MultiBodyIntegrator
        | integrators.PortHamiltonianIntegrator
        | integrators.EulerExplicit
        | integrators.EulerImplicit
        | integrators.Midpoint
        | integrators.MidpointPH
    ):

        return self._dynamically_instantiate(
            module=integrators,
            class_name=self.configuration.integrator.class_name,
            kwargs=self.configuration.integrator.kwargs,
        )

    def _set_time_stepper(
        self,
    ) -> (
        time_steppers.TimeStepper
        | time_steppers.FixedIncrement
        | time_steppers.FixedIncrementHittingEnd
    ):

        return self._dynamically_instantiate(
            module=time_steppers,
            class_name=self.configuration.time_stepper.class_name,
            kwargs=self.configuration.time_stepper.kwargs,
        )

    def _dynamically_instantiate(self, module, class_name, kwargs):

        # Deepcopy and handle empty kwargs
        kwargs = {} if (kwargs is None) else copy.deepcopy(kwargs)

        return getattr(
            module,
            class_name,
        )(manager=self, **kwargs)

    def manage(self):
        return self.solver.solve()
