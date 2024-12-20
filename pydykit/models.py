from typing import Literal, Union

from pydantic import BaseModel, Field, TypeAdapter, field_validator, model_validator
from typing_extensions import Annotated, Self


class ParticleSystem(BaseModel):
    pass
