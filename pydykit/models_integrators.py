from typing import Literal

from pydantic import NonNegativeFloat

from .models import Integrator


class MidpointPH(Integrator):
    class_name: Literal["MidpointPH"]


class MidpointMultibody(Integrator):
    class_name: Literal["MidpointMultibody"]


class MidpointDAE(Integrator):
    class_name: Literal["MidpointDAE"]


class DiscreteGradientBase(Integrator):

    increment_tolerance: NonNegativeFloat
    discrete_gradient_type: Literal[
        "Gonzalez_decomposed",
        "Gonzalez",
    ]


class DiscreteGradientPHDAE(DiscreteGradientBase):
    class_name: Literal["DiscreteGradientPHDAE"]


class DiscreteGradientMultibody(DiscreteGradientBase):
    class_name: Literal["DiscreteGradientMultibody"]
