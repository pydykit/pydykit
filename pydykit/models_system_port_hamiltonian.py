from typing import ClassVar, Literal

from pydantic import NonNegativeFloat

from .factories import factories
from .models import PydykitBaseModel, RegisteredClassName
from .utils import get_indices, sort_based_on_attribute


class State(PydykitBaseModel):
    angle: list[float]
    angular_velocity: list[float]


class Pendulum2D(PydykitBaseModel, RegisteredClassName):

    factory: ClassVar = factories["system"]
    class_name: Literal["Pendulum2D"]
    mass: NonNegativeFloat
    gravity: float
    length: NonNegativeFloat
    state: State
