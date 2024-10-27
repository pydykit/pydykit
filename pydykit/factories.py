from . import abstract_base_classes, results
from .integrators import Midpoint_DAE, MidpointODE, MidpointPH
from .results import Result
from .simulators import OneStep
from .systems_multi_body import ParticleSystem, RigidBodyRotatingQuaternions
from .systems_ode import Lorenz
from .systems_port_hamiltonian import Pendulum2D
from .time_steppers import FixedIncrement, FixedIncrementHittingEnd


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
        # TODO: Try to make the type hint of this method more specific, i.e.. return Factory().constructors[key]
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


class ResultFactory(Factory):
    def get(self, key, **kwargs) -> results.Result:
        return self.create(key, **kwargs)


system_factory = SystemFactory()
for key, constructor in [
    ("ParticleSystem", ParticleSystem),
    ("RigidBodyRotatingQuaternions", RigidBodyRotatingQuaternions),
    ("Pendulum2D", Pendulum2D),
    ("Lorenz", Lorenz),
]:
    system_factory.register_constructor(key=key, constructor=constructor)


simulator_factory = SimulatorFactory()
for key, constructor in [
    ("OneStep", OneStep),
]:
    simulator_factory.register_constructor(key=key, constructor=constructor)


integrator_factory = IntegratorFactory()
for key, constructor in [
    ("MidpointPH", MidpointPH),
    ("Midpoint_DAE", Midpoint_DAE),
    ("MidpointODE", MidpointODE),
]:
    integrator_factory.register_constructor(key=key, constructor=constructor)

time_stepper_factory = TimeStepperFactory()
for key, constructor in [
    ("FixedIncrement", FixedIncrement),
    ("FixedIncrementHittingEnd", FixedIncrementHittingEnd),
]:
    time_stepper_factory.register_constructor(key=key, constructor=constructor)

result_factory = ResultFactory()
for key, constructor in [
    ("Result", Result),
]:
    result_factory.register_constructor(key=key, constructor=constructor)
