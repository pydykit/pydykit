import copy

from . import integrators, results, solvers, systems, time_steppers, utils
from .configuration import Configuration


class Manager:

    def configure(self, configuration: Configuration):
        self._configure(configuration=configuration)

    def configure_from_path(self, path):
        file_content = utils.load_yaml_file(
            path=path,
        )
        configuration = Configuration(
            **file_content["configuration"],
        )

        self._configure(configuration=configuration)

    def _configure(self, configuration):

        # set configuration
        self.configuration = configuration

        # derive instances of classes
        self.time_stepper = self._set_time_stepper()
        self.solver = self._set_solver()
        self.integrator = self._set_integrator()
        self.system = self._set_system()
        self.result = self._set_result()

        # manager shuffles current and next state between objects
        self.current_state = self.next_state = self.system.state

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
        | integrators.Midpoint_DAE
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

    def _set_result(
        self,
    ) -> results.Result:

        return self._dynamically_instantiate(
            module=results,
            class_name="Result",
            kwargs=None,
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
