from pydantic import BaseModel


class ClassNameKwargs(BaseModel):
    class_name: str
    kwargs: dict | None


class Configuration(BaseModel):
    system: ClassNameKwargs
    solver: ClassNameKwargs
    integrator: ClassNameKwargs
    time_stepper: ClassNameKwargs
    state: ClassNameKwargs
