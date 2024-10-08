from pydantic import BaseModel


class ClassNameKwargs(BaseModel):
    class_name: str
    kwargs: dict | None


class Configuration(BaseModel):
    system: ClassNameKwargs
    simulator: ClassNameKwargs
    integrator: ClassNameKwargs
    time_stepper: ClassNameKwargs
