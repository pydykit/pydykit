from dependency_injector.wiring import Provide, inject

from . import abstract_base_classes, containers, utils
from .configuration import Configuration


class Manager(abstract_base_classes.Manager):

    @inject
    def __init__(
        self,
        configuration: Configuration = Provide[containers.Container.service],
        system=Provide[containers.Container.system],
        simulator=Provide[containers.Container.simulator],
        integrator=Provide[containers.Container.integrator],
        time_stepper=Provide[containers.Container.time_stepper],
        result=Provide[containers.Container.result],
    ):
        # set configuration
        self.configuration = configuration

        # derive instances of classes
        self.system = system
        self.simulator = simulator
        self.integrator = integrator
        self.time_stepper = time_stepper
        self.result = result

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
