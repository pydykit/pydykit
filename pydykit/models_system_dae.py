from typing import ClassVar, Literal

from annotated_types import Le, Len
from pydantic import NonNegativeFloat, PositiveFloat
from typing_extensions import Annotated

from .factories import factories
from .models import PydykitBaseModel, RegisteredClassName


class State(PydykitBaseModel):
    state: Annotated[
        list[float],
        Len(min_length=3, max_length=3),
    ]


class Lorenz(PydykitBaseModel, RegisteredClassName):

    factory: ClassVar = factories["system"]
    class_name: Literal["Lorenz"]
    sigma: PositiveFloat
    rho: PositiveFloat
    beta: PositiveFloat
    state: State


class ChemicalReactor(PydykitBaseModel, RegisteredClassName):
    factory: ClassVar = factories["system"]
    class_name: Literal["ChemicalReactor"]
    state: State
    constants: Annotated[
        list[float],
        Len(min_length=4, max_length=4),
    ]
    cooling_temperature: NonNegativeFloat
    reactant_concentration: Annotated[NonNegativeFloat, Le(1.0)]
    initial_temperature: NonNegativeFloat
