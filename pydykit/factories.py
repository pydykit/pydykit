from . import abstract_base_classes
from .simulators import OneStep
from .systems import Lorenz, ParticleSystem, Pendulum2D, RigidBodyRotatingQuaternions


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
