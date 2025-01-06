from typing import ClassVar, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .factories import factories
from .models import RegisteredClassName, ExtendableModel
from .models_system_dae import ChemicalReactor, Lorenz
from .models_system_multibody import ParticleSystem, RigidBodyRotatingQuaternions
from .models_system_port_hamiltonian import Pendulum2D


class Simulator(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["simulator"]


class Integrator(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["integrator"]


class TimeStepper(
    RegisteredClassName,
    ExtendableModel,
):
    factory: ClassVar = factories["time_stepper"]


class Configuration(BaseModel):
    system: Annotated[
        Union[
            ParticleSystem,
            RigidBodyRotatingQuaternions,
            Pendulum2D,
            Lorenz,
            ChemicalReactor,
        ],
        Field(discriminator="class_name"),
    ]
    simulator: Simulator
    integrator: Integrator
    time_stepper: TimeStepper
