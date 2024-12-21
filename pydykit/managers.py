from . import abstract_base_classes, results, utils
from .configuration import Configuration
from .factories import factories


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

        self.configuration = configuration

        # derive instances of classes
        for key in factories.keys():
            setattr(self, key, self.get_instance(key=key))

        # self.result = results.Result(manager=self)

    def get_instance(self, key):
        obj = getattr(self.configuration, key)
        factory = factories[key]

        return factory.get(
            key=obj.class_name,
            manager=self,
            **obj.kwargs.model_dump(),  # Note: kwargs is a pydantic BaseModel now, but had been a dict in the past
        )

    def manage(self, result):
        return self.simulator.run(result=result)

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
