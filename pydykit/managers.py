import copy
import importlib

from . import abstract_base_classes, results, utils
from .configuration import Configuration
from .factories import (
    integrator_factory,
    result_factory,
    simulator_factory,
    system_factory,
    time_stepper_factory,
)


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
        self.time_stepper = self._get_time_stepper()
        self.simulator = self._get_simulator()
        self.integrator = self._get_integrator()
        self.system = self._get_system()
        self.result = self._get_result()

    def _get_system(self) -> abstract_base_classes.System:
        return system_factory.get(
            key=self.configuration.system.class_name,
            manager=self,
            **self.configuration.system.kwargs,
        )

    def _get_simulator(self) -> abstract_base_classes.Simulator:

        return simulator_factory.get(
            key=self.configuration.simulator.class_name,
            manager=self,
            **self.configuration.simulator.kwargs,
        )

    def _get_integrator(self) -> abstract_base_classes.Integrator:
        kwargs = utils.handle_none_as_empty_dict(
            self.configuration.integrator.kwargs
        )  # TODO: Handly the problem of kwargs=None in Model validation using pydantic
        return integrator_factory.get(
            key=self.configuration.integrator.class_name,
            manager=self,
            **kwargs,
        )

    def _get_time_stepper(
        self,
    ) -> abstract_base_classes.TimeStepper:
        return time_stepper_factory.get(
            key=self.configuration.time_stepper.class_name,
            manager=self,
            **self.configuration.time_stepper.kwargs,
        )

    def _get_result(
        self,
    ) -> results.Result:
        # TODO: Do not break the pattern, i.e., move to config file it this is dynamic or move elsehwere if it is static, i.e., the same for all simulations
        return result_factory.get(
            key="Result",
            manager=self,
        )

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
