import abc
from typing import Iterator

import numpy as np


class TimeStep:
    def __init__(self, index, time, last_increment):
        self.index = index
        self.time = time
        self.last_increment = last_increment


class TimeStepper(abc.ABC):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    @abc.abstractmethod
    def make_steps(self) -> Iterator[TimeStep]:
        """Returns a Python generator which returns TimeStep objects"""

    @property
    @abc.abstractmethod
    def current_step(self) -> TimeStep:
        pass


class FixedIncrementHittingEnd(TimeStepper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.times = self.identify_times()
        self.nbr_timesteps = len(self.times)

    def make_steps(self):
        for index, time in enumerate(self.times):

            self._current_step = TimeStep(
                index=index,
                time=time,
                last_increment=time - self.times[index - 1],
            )
            yield self._current_step

    @property
    def current_step(self):
        return self._current_step

    def identify_times(self):
        tmp = np.arange(
            start=self.start,
            stop=self.end,
            step=self.stepsize,
            dtype=np.float64,
        )
        if tmp[-1] < self.end:
            tmp = np.append(tmp, self.end)
        return tmp
