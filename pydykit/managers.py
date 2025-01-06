from . import abstract_base_classes, results, utils
from .configuration import Configuration
from .factories import factories


class Manager(abstract_base_classes.Manager):
    """
    Methods:

        Args:
            configuration (Configuration): The configuration object to set up the manager.


        Args:
            path (str): The file path to the YAML configuration file.


        Args:
            configuration (Configuration): The configuration object to set up the manager.


        Args:
            key (str): The key to identify which instance to retrieve.

        Returns:
            object: The instance of the class corresponding to the key.

        Args:
            result (Result): The result object to be processed by the simulator.

        Returns:
            object: The result of the simulation.


        Raises:
            AssertionError: If the system and integrator parametrizations do not match.
            PydykitException: If either the integrator or system does not have a parametrization attribute.
    """

    def configure(self, configuration: Configuration):
        """
        Configures the manager with the given configuration.

        Parameters
        ----------
        configuration : Configuration
            The configuration object to set up the manager.
        """

        self._configure(configuration=configuration)

    def configure_from_path(self, path):
        """
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
        """
        Internal method to set the configuration and derive instances of classes.

        Parameters
        ----------
        configuration : Configuration
            The configuration object to set up the manager.
        """

        self.configuration = configuration

        # derive instances of classes
        for key in factories.keys():
            setattr(self, key, self.get_instance(key=key))

        # self.result = results.Result(manager=self)

    def get_instance(self, key):
        """
        Retrieves an instance of a class based on the configuration.

        Parameters
        ----------
        key : str
            The key to identify which instance to retrieve.

        Returns
        -------
        object
            The instance of the class corresponding to the key.
        """
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

    def manage(self, result):
        """
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
        return self.simulator.run(result=result)

    def validate_integrator_system_combination(self):
        """
        Validates the compatibility of the integrator and system based on their parametrization.

        Raises
        ------
        AssertionError
            If the system and integrator parametrizations do not match.
        PydykitException
            If either the integrator or system does not have a parametrization attribute.
        """

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
