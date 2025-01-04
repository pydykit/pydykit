from typing import ClassVar, Literal

from pydantic import NonNegativeFloat

from .factories import factories
from .models import PydykitBaseModel, RegisteredClassName


class MidpointPH(PydykitBaseModel, RegisteredClassName):
    factory: ClassVar = factories["integrator"]
    # NOTE: Attributes typed as ClassVar do not represent attributes, but can, e.g., be used during validation, see
    #       https://docs.pydantic.dev/latest/concepts/models/#automatically-excluded-attributes
    class_name: Literal["MidpointPH",]


class MidpointMultibody(PydykitBaseModel, RegisteredClassName):
    factory: ClassVar = factories["integrator"]
    class_name: Literal["MidpointMultibody",]


class MidpointDAE(PydykitBaseModel, RegisteredClassName):
    factory: ClassVar = factories["integrator"]
    class_name: Literal["MidpointDAE",]


class DiscreteGradientBase(PydykitBaseModel, RegisteredClassName):
    factory: ClassVar = factories["integrator"]
    increment_tolerance: NonNegativeFloat
    discrete_gradient_type: Literal["Gonzalez_decomposed", "Gonzalez"]


class DiscreteGradientPHDAE(DiscreteGradientBase):
    class_name: Literal["DiscreteGradientPHDAE",]


class DiscreteGradientMultibody(DiscreteGradientBase):
    class_name: Literal["DiscreteGradientMultibody",]
