from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Annotated

from .factories import factories
from .models import ParticleSystemKwargs, PydykitBaseModel

map_class_name_to_config_file_param = {
    "System": "system",
    "Simulator": "simulator",
    "Integrator": "integrator",
    "TimeStepper": "time_stepper",
}


# TODO #114: Get rid of nesting in config files to avoid having both ParticleSystem and ParticleSystemKwargs.
#       Switch to something flat, like
# system:
#   class_name: "ParticleSystem"
#   particles: {}
#   springs: {}

# TODO #114: Consider removing the nesting "configuration"


class RegisteredClassName(BaseModel):
    class_name: str

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
    # TODO #115: Remove placeholder: This is a temporary placeholder to allow passing any arguments to classes which are not yet granularly pydantic validated.
    # This object is a BaseModel which can be assigned any attributes.
    model_config = ConfigDict(extra="allow")


class Simulator(RegisteredClassName):
    kwargs: Kwargs


class Integrator(RegisteredClassName):
    kwargs: Kwargs


class TimeStepper(RegisteredClassName):
    kwargs: Kwargs


class System(RegisteredClassName):
    class_name: Literal[
        "RigidBodyRotatingQuaternions",
        "Pendulum2D",
        "Lorenz",
        "ChemicalReactor",
    ]
    kwargs: Kwargs


class ParticleSystem(PydykitBaseModel):
    class_name: Literal["ParticleSystem"]
    kwargs: ParticleSystemKwargs

    @field_validator("class_name")
    def validate_that_class_name_refers_to_registered_factory_method(
        cls, class_name, info
    ):
        assert (
            class_name in factories["system"].constructors
        ), f"Can't find registered factory method for class_name={class_name}"

        return class_name


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
