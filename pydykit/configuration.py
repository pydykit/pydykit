from typing import ClassVar, Union

from pydantic import BaseModel, ConfigDict

from .factories import factories
from .models import RegisteredClassName
from .models_simulators import OneStep
from .models_system_dae import ChemicalReactor, Lorenz
from .models_system_multibody import ParticleSystem, RigidBodyRotatingQuaternions
from .models_system_port_hamiltonian import Pendulum2D
from .models_time_steppers import FixedIncrement, FixedIncrementHittingEnd


class ExtendableModel(BaseModel):
    # TODO #115: Remove placeholder: This is a temporary placeholder to allow passing any arguments to classes which are not yet granularly pydantic validated.
    # This object is a BaseModel which can be assigned any attributes.
    model_config = ConfigDict(extra="allow")


class Integrator(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["integrator"]
    # NOTE: Attributes typed as ClassVar do not represent attributes, but can, e.g., be used during validation, see
    #       https://docs.pydantic.dev/latest/concepts/models/#automatically-excluded-attributes


class Configuration(BaseModel):
    system: Union[
        ParticleSystem,
        RigidBodyRotatingQuaternions,
        Pendulum2D,
        Lorenz,
        ChemicalReactor,
    ]
    simulator: OneStep
    integrator: Integrator
    time_stepper: Union[FixedIncrement, FixedIncrementHittingEnd]
