from enum import Enum

from pydantic import BaseModel, field_validator

from .factories import (
    integrator_factory,
    simulator_factory,
    system_factory,
    time_stepper_factory,
)

valid_options = dict(
    System=system_factory.constructors,
    Simulator=simulator_factory.constructors,
    Integrator=integrator_factory.constructors,
    TimeStepper=time_stepper_factory.constructors,
)


class ClassNameKwargs(BaseModel):
    class_name: str
    kwargs: dict

    @field_validator("class_name")
    def validator(cls, class_name, info):

        title_base_model = info.config["title"]
        # Example: During validation of any field of model "System",
        # the expression "info.config['title'] will return 'System'"

        options = valid_options[title_base_model]

        if class_name not in options:
            raise ValueError(
                f"supported options for {title_base_model} are {options.keys()}"
            )

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
