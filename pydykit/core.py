import copy
import importlib

from . import utils


class Manager:
    def __init__(self, path_config_file=None, content_config_file=None):

        if (path_config_file is not None) and (content_config_file is not None):
            raise utils.pydykitException(
                "Did receive both path_config_file and content_config_file. "
                + "Supply either path_config_file or content_config_file, not both"
            )
        elif path_config_file is not None:
            self.path_config_file = path_config_file
            self.content_config_file = self.read_config_file()
        elif content_config_file is not None:
            self.content_config_file = content_config_file
        else:
            raise utils.pydykitException(
                "Did not receive kwargs. "
                + "Supply either path_config_file or content_config_file"
            )

        self.name = self.content_config_file["name"]
        self.configuration = self.content_config_file["configuration"]

        self.instantiate_classes()

    def read_config_file(self):
        return utils.load_yaml_file(path=self.path_config_file)

    def instantiate_classes(self):
        for attribute_name, parameters in self.configuration.items():
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

            setattr(
                self,
                attribute_name,
                cls(**kwargs),
            )

    def manage(self):
        return self.solver.solve()

    def postprocess(self, df):
        return self.postprocessor.postprocess(df)
