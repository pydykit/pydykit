from typing import Literal

from annotated_types import Le, Len
from pydantic import NonNegativeFloat, PositiveFloat
from typing_extensions import Annotated

from .models import PydykitBaseModel, SystemModel


class State(PydykitBaseModel):
    state: Annotated[
        list[float],
        Len(
            min_length=3,
            max_length=3,
        ),
    ]


class Lorenz(SystemModel):
    class_name: Literal["Lorenz"]

    sigma: PositiveFloat
    rho: PositiveFloat
    beta: PositiveFloat
    state: State


class ChemicalReactor(SystemModel):
    class_name: Literal["ChemicalReactor"]

    state: State
    constants: Annotated[
        list[float],
        Len(
            min_length=4,
            max_length=4,
        ),
    ]
    cooling_temperature: NonNegativeFloat
    reactant_concentration: Annotated[
        NonNegativeFloat,
        Le(1.0),
    ]
    initial_temperature: NonNegativeFloat
