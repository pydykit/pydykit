from typing import Literal

from pydantic import PositiveFloat, model_validator

from .models import TimeStepperModel


class FixedIncrementBase(TimeStepperModel):
    step_size: PositiveFloat
    start: float
    end: float

    @model_validator(mode="after")
    def check_end_greater_than_start(self):
        if self.end <= self.start:
            raise ValueError("end must be greater than start")
        return self


class FixedIncrement(FixedIncrementBase):
    class_name: Literal["FixedIncrement"]


class FixedIncrementHittingEnd(FixedIncrementBase):
    class_name: Literal["FixedIncrementHittingEnd"]
