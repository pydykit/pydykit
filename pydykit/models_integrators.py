from typing import Literal

from pydantic import NonNegativeFloat

from .models import IntegratorModel


class MidpointPH(IntegratorModel):
    class_name: Literal["MidpointPH"]


class MidpointMultibody(IntegratorModel):
    class_name: Literal["MidpointMultibody"]


class MidpointDAE(IntegratorModel):
    class_name: Literal["MidpointDAE"]


class DiscreteGradientBase(IntegratorModel):

    increment_tolerance: NonNegativeFloat
    discrete_gradient_type: Literal[
        "Gonzalez_decomposed",
        "Gonzalez",
    ]


class DiscreteGradientPHDAE(DiscreteGradientBase):
    class_name: Literal["DiscreteGradientPHDAE"]


class DiscreteGradientMultibody(DiscreteGradientBase):
    class_name: Literal["DiscreteGradientMultibody"]
