from typing import Literal

from pydantic import NonNegativeFloat, PositiveInt

from .models import Simulator


class OneStep(Simulator):
    solver_name: Literal[
        "NewtonPlainPython",
        "RootScipy",
    ]

    newton_epsilon: NonNegativeFloat
    max_iterations: PositiveInt
