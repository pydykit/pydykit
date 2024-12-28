from typing import ClassVar, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Annotated

from .factories import factories
from .models import ParticleSystemKwargs, PydykitBaseModel

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
    def validate_that_class_name_value_refers_to_registered_factory_method(
        cls,
        class_name,
        info,
    ):

        constructors = (
            cls.factory.constructors
        )  # Assumes that current model has a ClassVar attribute representing the factory

        if class_name not in constructors:
            raise ValueError(f"supported factory methods are {constructors.keys()}")

        return class_name


class Kwargs(BaseModel):
    # TODO #115: Remove placeholder: This is a temporary placeholder to allow passing any arguments to classes which are not yet granularly pydantic validated.
    # This object is a BaseModel which can be assigned any attributes.
    model_config = ConfigDict(extra="allow")


class Simulator(RegisteredClassName):
    factory: ClassVar = factories["simulator"]
    # NOTE: Attributes typed as ClassVar do not represent attributes, but can, e.g., be used during validation, see
    #       https://docs.pydantic.dev/latest/concepts/models/#automatically-excluded-attributes

    kwargs: Kwargs


class Integrator(RegisteredClassName):
    factory: ClassVar = factories["integrator"]

    kwargs: Kwargs


class TimeStepper(RegisteredClassName):
    factory: ClassVar = factories["time_stepper"]

    kwargs: Kwargs


class System(RegisteredClassName):
    factory: ClassVar = factories["system"]

    class_name: Literal[
        "RigidBodyRotatingQuaternions",
        "Pendulum2D",
        "Lorenz",
        "ChemicalReactor",
    ]
    kwargs: Kwargs


class ParticleSystem(PydykitBaseModel, RegisteredClassName):
    factory: ClassVar = factories["system"]

    class_name: Literal["ParticleSystem"]
    kwargs: ParticleSystemKwargs


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
