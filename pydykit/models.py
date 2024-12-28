from typing import Literal, Union

from annotated_types import Len
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    TypeAdapter,
    field_validator,
    model_validator,
)
from typing_extensions import Annotated, Self

from .utils import get_indices, sort_based_on_attribute


class PydykitBaseModel(BaseModel):
    # Forbid extra attributes of this class, see https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra
    model_config = ConfigDict(extra="forbid")


class Particle(PydykitBaseModel):
    index: int
    initial_position: list[float]
    initial_momentum: list[float]
    mass: NonNegativeFloat


class Ending(PydykitBaseModel):
    type: Literal["support", "particle"]
    index: int


class Spring(PydykitBaseModel):
    start: Ending
    end: Ending
    stiffness: float
    equilibrium_length: NonNegativeFloat


class Support(PydykitBaseModel):
    index: int
    type: Literal["fixed"]
    position: list[float]


class Damper(PydykitBaseModel):
    start: Ending
    end: Ending
    ground_viscosity: NonNegativeFloat
    state_dependent: bool
    alpha: NonNegativeFloat


class Constraint(PydykitBaseModel):
    start: Ending
    end: Ending
    length: NonNegativeFloat


class ParticleSystemKwargs(PydykitBaseModel):

    nbr_spatial_dimensions: Literal[1, 2, 3]

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
    def enforce_springs_endings_are_valid(self):
        valid_options = ["particle", "support"]
        for spring in self.springs:
            for ending in ["start", "end"]:
                assert (
                    getattr(spring, ending).type in valid_options
                ), f"Spring endings have to be of one of these types: {valid_options}"
        return self

    @model_validator(mode="after")
    def sort_particles_and_supports(self):
        self.particles = sort_based_on_attribute(
            obj=self.particles,
            attribute="index",
        )
        self.supports = sort_based_on_attribute(
            obj=self.supports,
            attribute="index",
        )
        return self

    @model_validator(mode="after")
    def enforce_particle_and_support_indices_to_be_sorted_start_at_zero_and_be_consecutive(
        self,
    ):

        workload = {}
        for group in ["particles", "supports"]:
            items = getattr(self, group)
            # Only add to workload, if not empty list
            if items != []:
                workload.update({group: get_indices(items)})

        for group, indices in workload.items():

            message_start = f"{group}-indices should "

            assert sorted(indices) == indices, (
                message_start + f"be sorted, but found {indices}"
            )
            assert min(indices) == 0, (
                message_start + f"start at zero, but found {indices}"
            )
            assert indices == list(range(min(indices), max(indices) + 1)), (
                message_start + f"be consecutive, but found {indices}"
            )

        return self

    @model_validator(mode="after")
    def enforce_existence_of_indices(self):

        particle_indices = get_indices(self.particles)
        support_indices = get_indices(self.supports)

        indices = {
            "particle": particle_indices,
            "support": support_indices,
        }

        for group in ["springs", "dampers", "constraints"]:
            for item in getattr(self, group):
                for ending_key in ["start", "end"]:
                    ending = getattr(item, ending_key)

                    message = (
                        f"Could not find {ending.type} "
                        + f"with index={ending.index} "
                        + f"requested by attribute '{ending_key}' in {group} object \t'{item}'."
                    )

                    assert ending.index in indices[ending.type], message

        return self
