from enum import Enum

from pydantic import BaseModel, field_validator

from .factories import factories

map_class_name_to_config_file_param = {
    "System": "system",
    "Simulator": "simulator",
    "Integrator": "integrator",
    "TimeStepper": "time_stepper",
}


class ClassNameKwargs(BaseModel):
    class_name: str
    kwargs: dict

    @field_validator("class_name")
    def validator(cls, class_name, info):

        title = info.config["title"]
        # Example: During validation of any field of model "System",
        # the expression "info.config['title'] will return 'System'"

        key = map_class_name_to_config_file_param[title]
        options = factories[key].constructors

        if class_name not in options:
            raise ValueError(f"supported options for {title} are {options.keys()}")

        return class_name


class System(ClassNameKwargs):
    pass


class Simulator(ClassNameKwargs):
    pass


class Integrator(ClassNameKwargs):
    pass


class TimeStepper(ClassNameKwargs):
    pass


class Configuration(BaseModel):
    system: System
    simulator: Simulator
    integrator: Integrator
    time_stepper: TimeStepper
