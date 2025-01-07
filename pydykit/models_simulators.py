from typing import Literal

from pydantic import NonNegativeFloat, PositiveInt

from .models import SimulatorModel


class OneStep(SimulatorModel):
    solver_name: Literal[
        "NewtonPlainPython",
        "RootScipy",
    ]

    newton_epsilon: NonNegativeFloat
    max_iterations: PositiveInt
