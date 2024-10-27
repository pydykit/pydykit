from enum import Enum

from pydantic import BaseModel, field_validator

from .factories import integrator_factory


class ClassNameKwargs(BaseModel):
    class_name: str
    kwargs: dict | None


class Integrator(ClassNameKwargs):

    @field_validator("class_name")
    def validator(cls, arg):
        options = integrator_factory.constructors
        if arg not in options:
            raise ValueError(f"supported options are {options}")
        return arg


class Configuration(BaseModel):
    system: ClassNameKwargs
    simulator: ClassNameKwargs
    integrator: Integrator
    time_stepper: ClassNameKwargs
