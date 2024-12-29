from typing import ClassVar, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Annotated

from .factories import factories
from .models import PydykitBaseModel, RegisteredClassName
from .models_system import ParticleSystem


class ExtendableModel(BaseModel):
    # TODO #115: Remove placeholder: This is a temporary placeholder to allow passing any arguments to classes which are not yet granularly pydantic validated.
    # This object is a BaseModel which can be assigned any attributes.
    model_config = ConfigDict(extra="allow")


class Simulator(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["simulator"]
    # NOTE: Attributes typed as ClassVar do not represent attributes, but can, e.g., be used during validation, see
    #       https://docs.pydantic.dev/latest/concepts/models/#automatically-excluded-attributes


class Integrator(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["integrator"]


class TimeStepper(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["time_stepper"]


class System(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["system"]

    class_name: Literal[
        "RigidBodyRotatingQuaternions",
        "Pendulum2D",
        "Lorenz",
        "ChemicalReactor",
    ]


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
