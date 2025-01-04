from typing import ClassVar, Literal

from pydantic import NonNegativeFloat, PositiveInt

from .factories import factories
from .models import PydykitBaseModel, RegisteredClassName


class OneStep(PydykitBaseModel, RegisteredClassName):
    factory: ClassVar = factories["simulator"]
    solver_name: Literal[
        "NewtonPlainPython",
        "RootScipy",
    ]
    newton_epsilon: NonNegativeFloat
    max_iterations: PositiveInt
