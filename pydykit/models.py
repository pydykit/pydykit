from typing import Literal, Union

from annotated_types import Len
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    field_validator,
    model_validator,
)
from typing_extensions import Annotated, Self

from .factories import factories


class Simulator(BaseModel):
    class_name: str
    kwargs: dict


class Integrator(BaseModel):
    class_name: str
    kwargs: dict


class TimeStepper(BaseModel):
    class_name: str
    kwargs: dict


class System(BaseModel):
    class_name: Literal[
        "RigidBodyRotatingQuaternions",
        "Pendulum2D",
        "Lorenz",
        "ChemicalReactor",
    ]
    kwargs: dict


# TODO: Get rid of nesting in config files to avoid having both ParticleSystem and ParticleSystemKwargs.
#       Switch to something flat, like
# system:
#   class_name: "ParticleSystem"
#   particles: {}
#   springs: {}

# TODO: Consider removing the nesting "configuration"


class PydykitBaseModel(BaseModel):
    # Forbid extra attributes of this class, this should be the default for all systems kwargs to be rather strict
    model_config = ConfigDict(extra="forbid")


class Particle(PydykitBaseModel):
    index: int
    initial_position: list[float]
    initial_momentum: list[float]
    mass: float


class Spring(PydykitBaseModel):
    particle_start: int
    particle_end: int
    stiffness: float
    equilibrium_length: float


class Support(PydykitBaseModel):
    index: int
    type: Literal["fixed"]
    position: list[float]


class Ending(PydykitBaseModel):
    type: Literal["fixed", "particle"]
    index: int


class Damper(PydykitBaseModel):
    start: Ending
    end: Ending
    ground_viscosity: float
    state_dependent: bool
    alpha: float


class Constraint(PydykitBaseModel):
    start: Ending
    end: Ending
    length: float


class ParticleSystemKwargs(PydykitBaseModel):

    # TODO: Discuss whether this should be set to values [1, 2, 3]
    nbr_spatial_dimensions: int

    particles: Annotated[
        list[Particle],
        Len(min_length=1),
    ]

    supports: list[Support]
    springs: list[Spring]
    dampers: list[Damper]
    constraints: list[Constraint]

    gravity: list[float]

    @model_validator(mode="after")
    def enforce_dimensions(self):
        dim = self.nbr_spatial_dimensions
        message = "Dimensions have to be met"

        for particle in self.particles:
            assert all(
                [
                    len(particle.initial_position) == dim,
                    len(particle.initial_momentum) == dim,
                ]
            ), message

        for support in self.supports:
            assert len(support.position) == dim, message

        assert len(self.gravity) == dim, message

        return self

    @model_validator(mode="after")
    def enforce_existence_of_indices(self):
        # TODO: Implement this on particles and supports referenced from endingsin springs, dampers, constraints
        return self

    @model_validator(mode="after")
    def enforce_indices_to_be_consecutive(self):
        # TODO: Implement this on particles and supports
        return self


class ParticleSystem(BaseModel):
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
