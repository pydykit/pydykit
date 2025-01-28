from . import abstract_base_classes, results, utils
from .configuration import Configuration
from .factories import factories
from .results import Result


class Manager(abstract_base_classes.Manager):
    """TODO: Validate docstring

    Methods:
        __init__: Get going
        configure: Bla
    """

    def configure(self, configuration: Configuration):
        """
        TODO: Validate docstring
        Configures the manager with the given configuration.

        Parameters
        ----------
        configuration : Configuration
            The configuration object to set up the manager.

        Examples:
            Some explanation of what is possible.

            >>> print("hello!")
            hello!

            Blank lines delimit prose vs. console blocks.

            >>> a = 0
            >>> a += 1
            >>> a
            1


        Note:
            Some information.

        """

        self._configure(configuration=configuration)

    def configure_from_path(self, path):
        """
        TODO: Validate docstring
        Loads configuration from a YAML file and configures the manager.

        Parameters
        ----------
        path : str
            The file path to the YAML configuration file.
        """
        file_content = utils.load_yaml_file(
            path=path,
        )
        configuration = Configuration(
            **file_content,
        )

        self._configure(configuration=configuration)

    def _configure(self, configuration):

        self.configuration = configuration

        # derive instances of classes
        for key in factories.keys():
            setattr(self, key, self._get_instance(key=key))

        # self.result = results.Result(manager=self)

    def _get_instance(self, key):

        obj = getattr(self.configuration, key)
        factory = factories[key]

        kwargs = obj.model_dump()
        kwargs.pop(
            "class_name"
        )  # Remove discriminator entry "class_name" from kwargs passed to constructor

        return factory.get(
            key=obj.class_name,
            manager=self,
            **kwargs,
        )

    def manage(self, result=None) -> Result:
        """
        TODO: Validate docstring
        Runs the simulator with the given result.

        Parameters
        ----------
        result : Result
            The result object to be processed by the simulator.

        Returns
        -------
        object
            The result of the simulation.
        """
        if result is None:
            result = Result(manager=self)

        return self.simulator.run(result=result)

    def _validate_integrator_system_combination(self):

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
