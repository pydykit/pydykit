from typing import Literal

from pydantic import NonNegativeFloat

from .models import PydykitBaseModel, SystemModel


class State(PydykitBaseModel):
    angle: list[float]
    angular_velocity: list[float]


class Pendulum2D(SystemModel):
    class_name: Literal["Pendulum2D"]

    mass: NonNegativeFloat
    gravity: float
    length: NonNegativeFloat
    state: State
