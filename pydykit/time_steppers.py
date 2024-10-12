from itertools import pairwise

import numpy as np

from . import abstract_base_classes, utils


class TimeStep(abstract_base_classes.TimeStep):
    def __init__(self, index: int, time: float, increment: float):
        self.index = index
        self.time = time
        self.increment = (
            increment  # this is next point in time minus current point in time
        )


class TimeStepper(abstract_base_classes.TimeStepper):
    def __init__(self, manager, step_size: float, start: float, end: float):
        self.manager = manager
        self.step_size = step_size
        self.start = start
        self.end = end


class FixedIncrement(TimeStepper):
    def __init__(self, manager, step_size: float, start: float, end: float):

        super().__init__(
            start=start,
            end=end,
            step_size=step_size,
            manager=manager,
        )

        self.nbr_steps = int((self.end - self.start) / self.step_size)
        self.nbr_time_points = self.nbr_steps + 1

        self.times = self.identify_times()

        self.step_size = self.get_step_size()

    @property
    def current_step(self):
        return self._current_step

    def make_steps(self):
        for index, time in enumerate(self.times):

            self._current_step = TimeStep(
                index=index,
                time=time,
                increment=self.step_size,  # fixed time step size
            )
            yield self._current_step

    def identify_times(self):
        return np.linspace(
            start=self.start,
            stop=self.end,
            num=self.nbr_time_points,
            endpoint=True,
            dtype=np.float64,
        )

    def get_step_size(self):

        step_sizes = np.array([n1 - n for n, n1 in pairwise(self.times)])
        step_size = step_sizes[0]

        step_sizes_all_equal = np.all(np.isclose(step_sizes, step_size))

        assert (
            step_sizes_all_equal
        ), "Implementation should yield homogeneous time steps"

        return step_size


class FixedIncrementHittingEnd(TimeStepper):
    def __init__(self, start, end, step_size, manager):

        super().__init__(
            start=start,
            end=end,
            step_size=step_size,
            manager=manager,
        )

        self.times = self.identify_times()
        self.nbr_time_points = len(self.times)
        self.nbr_steps = self.nbr_time_points - 1

    def make_steps(self):
        for index, time in enumerate(self.times):

            self._current_step = TimeStep(
                index=index,
                time=time,
                increment=time - self.times[index - 1],  # variable time step size
            )
            yield self._current_step

    @property
    def current_step(self):
        return self._current_step

    def identify_times(self):
        tmp = np.arange(
            start=self.start,
            stop=self.end,
            step=self.step_size,
            dtype=np.float64,
        )

        if tmp[-1] < self.end:
            # If expected end time is not reached, add it as last step
            tmp = np.append(tmp, self.end)
        elif np.isclose(tmp[-1], self.end):
            pass
        else:
            raise utils.PydykitException("Unkown case")

        return tmp
