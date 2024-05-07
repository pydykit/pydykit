import abc


class TimeStepper(abc.ABC):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)


class FixedIncrement(TimeStepper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbr_timesteps = int((self.end - self.start) / self.stepsize)
