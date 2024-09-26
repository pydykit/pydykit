import copy
import importlib

from . import utils


class Manager:
    def __init__(self, path_config_file=None, content_config_file=None):

        utils.update_object_from_config_file(
            self, path_config_file, content_config_file
        )

        self.instantiate_classes()

    def read_config_file(self):
        return utils.load_yaml_file(path=self.path_config_file)

    def instantiate_classes(self):
        for attribute_name, parameters in self.configuration.items():
            # Get class from module
            cls = getattr(
                importlib.import_module(
                    name=f".{attribute_name}s",
                    package="pydykit",
                ),
                parameters["class_name"],
            )

            # Handle empty kwargs
            kwargs = (
                {}
                if (parameters["kwargs"] is None)
                else copy.deepcopy(parameters["kwargs"])
            )
            # Add manager to all classes to be able to access other class instances through manager
            kwargs.update(dict(manager=self))

            # Create instance
            instance = cls(**kwargs)

            # Set instance to manager
            setattr(
                self,
                attribute_name,
                instance,
            )

    def manage(self):
        return self.solver.solve()
