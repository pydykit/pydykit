from typing import Union

from pydantic import BaseModel, ConfigDict

from .models_integrators import (
    DiscreteGradientMultibody,
    DiscreteGradientPHDAE,
    MidpointDAE,
    MidpointMultibody,
    MidpointPH,
)
from .models_simulators import OneStep
from .models_system_dae import ChemicalReactor, Lorenz
from .models_system_multibody import ParticleSystem, RigidBodyRotatingQuaternions
from .models_system_port_hamiltonian import Pendulum2D
from .models_time_steppers import FixedIncrement, FixedIncrementHittingEnd


class ExtendableModel(BaseModel):
    # TODO #115: Remove placeholder: This is a temporary placeholder to allow passing any arguments to classes which are not yet granularly pydantic validated.
    # This object is a BaseModel which can be assigned any attributes.
    model_config = ConfigDict(extra="allow")


class Configuration(BaseModel):
    system: Union[
        ParticleSystem,
        RigidBodyRotatingQuaternions,
        Pendulum2D,
        Lorenz,
        ChemicalReactor,
    ]
    simulator: OneStep
    integrator: Union[
        MidpointPH,
        DiscreteGradientPHDAE,
        MidpointMultibody,
        DiscreteGradientMultibody,
        MidpointDAE,
    ]
    time_stepper: Union[FixedIncrement, FixedIncrementHittingEnd]
