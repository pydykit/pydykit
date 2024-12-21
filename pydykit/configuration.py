from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Annotated

from .factories import factories
from .models import ParticleSystem

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
    def validate_that_class_name_refers_to_registered_factory_method(
        cls, class_name, info
    ):

        title = info.config["title"]
        # Example: During validation of any field of model "System",
        # the expression "info.config['title'] will return 'System'"

        key = map_class_name_to_config_file_param[title]
        options = factories[key].constructors

        if class_name not in options:
            raise ValueError(f"supported options for {title} are {options.keys()}")

        return class_name


class Kwargs(BaseModel):
    # This is a temporary placeholder to allow passing any arguments to classes which are not yet granularly pydantic validated.
    # This object is a BaseModel which can be assigned any attributes.
    model_config = ConfigDict(extra="allow")


class Simulator(ClassNameKwargs):
    kwargs: Kwargs


class Integrator(ClassNameKwargs):
    kwargs: Kwargs


class TimeStepper(ClassNameKwargs):
    kwargs: Kwargs


class System(ClassNameKwargs):
    class_name: Literal[
        "RigidBodyRotatingQuaternions",
        "Pendulum2D",
        "Lorenz",
        "ChemicalReactor",
    ]
    kwargs: Kwargs


class Configuration(BaseModel):
    system: Annotated[
        Union[
            System,
            ParticleSystem,
        ],
        Field(discriminator="class_name"),
    ]
    simulator: Simulator
    integrator: Integrator
    time_stepper: TimeStepper
