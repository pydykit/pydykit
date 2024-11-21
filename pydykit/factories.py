from . import abstract_base_classes
from .integrators import (
    DiscreteGradientMultibody,
    DiscreteGradientPHDAE,
    MidpointDAE,
    MidpointMultibody,
    MidpointPH,
)
from .simulators import OneStep
from .systems_dae import ChemicalReactor, Lorenz
from .systems_multi_body import ParticleSystem, RigidBodyRotatingQuaternions
from .systems_port_hamiltonian import Pendulum2D
from .time_steppers import FixedIncrement, FixedIncrementHittingEnd

registered_systems = {
    "ParticleSystem": ParticleSystem,
    "RigidBodyRotatingQuaternions": RigidBodyRotatingQuaternions,
    "Pendulum2D": Pendulum2D,
    "Lorenz": Lorenz,
    "ChemicalReactor": ChemicalReactor,
}

registered_simulators = {"OneStep": OneStep}

registered_integrators = {
    "MidpointPH": MidpointPH,
    "DiscreteGradientPHDAE": DiscreteGradientPHDAE,
    "MidpointMultibody": MidpointMultibody,
    "DiscreteGradientMultibody": DiscreteGradientMultibody,
    "MidpointDAE": MidpointDAE,
}

registered_timesteppers = {
    "FixedIncrement": FixedIncrement,
    "FixedIncrementHittingEnd": FixedIncrementHittingEnd,
}


class Factory:

    def __init__(self):
        self.constructors = {}

    def register_constructor(self, key, constructor):
        self.constructors[key] = constructor

    def create(self, key, **kwargs):
        method = self.constructors[key]
        return method(**kwargs)


class SystemFactory(Factory):
    def get(self, key, **kwargs) -> abstract_base_classes.System:
        return self.create(key, **kwargs)


class SimulatorFactory(Factory):
    def get(self, key, **kwargs) -> abstract_base_classes.Simulator:
        return self.create(key, **kwargs)


class IntegratorFactory(Factory):
    def get(self, key, **kwargs) -> abstract_base_classes.Integrator:
        return self.create(key, **kwargs)


class TimeStepperFactory(Factory):
    def get(self, key, **kwargs) -> abstract_base_classes.TimeStepper:
        return self.create(key, **kwargs)


system_factory = SystemFactory()
for key, constructor in registered_systems.items():
    system_factory.register_constructor(key=key, constructor=constructor)


simulator_factory = SimulatorFactory()
for key, constructor in registered_simulators.items():
    simulator_factory.register_constructor(key=key, constructor=constructor)


integrator_factory = IntegratorFactory()
for key, constructor in registered_integrators.items():
    integrator_factory.register_constructor(key=key, constructor=constructor)

time_stepper_factory = TimeStepperFactory()
for key, constructor in registered_timesteppers.items():
    time_stepper_factory.register_constructor(key=key, constructor=constructor)

factories = dict(
    system=system_factory,
    simulator=simulator_factory,
    integrator=integrator_factory,
    time_stepper=time_stepper_factory,
)
