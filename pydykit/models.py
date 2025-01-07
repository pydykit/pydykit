from typing import ClassVar

from pydantic import BaseModel, ConfigDict, field_validator

from .factories import factories


class PydykitBaseModel(BaseModel):
    # Forbid extra attributes of this class, see https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra
    model_config = ConfigDict(extra="forbid")


class RegisteredClassName(BaseModel):
    class_name: str

    @field_validator("class_name")
    def validate_that_class_name_value_refers_to_registered_factory_method(
        cls,
        class_name,
        info,
    ):

        constructors = (
            cls.factory.constructors
        )  # Assumes that current model has a ClassVar attribute representing the factory

        if class_name not in constructors:
            raise ValueError(f"supported factory methods are {constructors.keys()}")

        return class_name


class SystemModel(
    RegisteredClassName,
    PydykitBaseModel,
):
    # NOTE: Attributes typed as ClassVar do not represent attributes, but can, e.g., be used during validation, see
    #       https://docs.pydantic.dev/latest/concepts/models/#automatically-excluded-attributes
    factory: ClassVar = factories["system"]


class IntegratorModel(
    RegisteredClassName,
    PydykitBaseModel,
):
    factory: ClassVar = factories["integrator"]


class SimulatorModel(
    RegisteredClassName,
    PydykitBaseModel,
):
    factory: ClassVar = factories["simulator"]


class TimeStepperModel(
    RegisteredClassName,
    PydykitBaseModel,
):
    factory: ClassVar = factories["time_stepper"]
