from typing import Union

from pydantic import BaseModel

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
