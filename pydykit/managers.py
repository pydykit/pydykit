import copy
import importlib

from . import abstract_base_classes, results, utils
from .configuration import Configuration


class Manager(abstract_base_classes.Manager):

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
        self.simulator = self._set_simulator()
        self.integrator = self._set_integrator()
        self.system = self._set_system()
        self.result = self._set_result()

    def _set_system(
        self,
    ) -> abstract_base_classes.System:

        return self._dynamically_instantiate(
            module_name="systems",
            class_name=self.configuration.system.class_name,
            kwargs=self.configuration.system.kwargs,
        )

    def _set_simulator(self) -> abstract_base_classes.Simulator:

        return self._dynamically_instantiate(
            module_name="simulators",
            class_name=self.configuration.simulator.class_name,
            kwargs=self.configuration.simulator.kwargs,
        )

    def _set_integrator(
        self,
    ) -> abstract_base_classes.Integrator:

        return self._dynamically_instantiate(
            module_name="integrators",
            class_name=self.configuration.integrator.class_name,
            kwargs=self.configuration.integrator.kwargs,
        )

    def _set_time_stepper(
        self,
    ) -> abstract_base_classes.TimeStepper:

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
        return self.simulator.run()

    def validate_integrator_system_combination(self):

        if hasattr(self.integrator, "parametrization") and hasattr(
            self.system, "parametrization"
        ):
            assert (
                self.system.parametrization == self.integrator.parametrization
            ), "System and integrator are not compatible."

        else:
            raise utils.PydykitException(
                "Could not validate compatibilty of system and integrator."
                + " Integrator does not have attribute `parametrization`"
                + " System does not have attribute `parametrization`"
            )
