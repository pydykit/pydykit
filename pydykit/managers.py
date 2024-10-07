import copy
import importlib

from . import base_classes, results, utils
from .configuration import Configuration


class Manager(base_classes.Manager):

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
        self.current_state = self.system.state

    def _set_system(
        self,
    ) -> (
        base_classes.AbstractMultiBodySystem
        | base_classes.AbstractPortHamiltonianSystem
    ):

        return self._dynamically_instantiate(
            module_name="systems",
            class_name=self.configuration.system.class_name,
            kwargs=self.configuration.system.kwargs,
        )

    def _set_solver(self) -> base_classes.Solver:

        return self._dynamically_instantiate(
            module_name="solvers",
            class_name=self.configuration.solver.class_name,
            kwargs=self.configuration.solver.kwargs,
        )

    def _set_integrator(
        self,
    ) -> base_classes.Integrator:

        return self._dynamically_instantiate(
            module_name="integrators",
            class_name=self.configuration.integrator.class_name,
            kwargs=self.configuration.integrator.kwargs,
        )

    def _set_time_stepper(
        self,
    ) -> base_classes.TimeStepper:

        return self._dynamically_instantiate(
            module_name="time_steppers",
            class_name=self.configuration.time_stepper.class_name,
            kwargs=self.configuration.time_stepper.kwargs,
        )

    def _set_result(
        self,
    ) -> results.Result:

        return self._dynamically_instantiate(
            module_name="results",
            class_name="Result",
            kwargs=None,
        )

    def _dynamically_instantiate(self, module_name, class_name, kwargs):

        # Deepcopy and handle empty kwargs
        kwargs = {} if (kwargs is None) else copy.deepcopy(kwargs)

        return getattr(
            importlib.import_module(
                name=f".{module_name}",
                package="pydykit",
            ),
            class_name,
        )(manager=self, **kwargs)

    def manage(self):
        return self.solver.solve()
