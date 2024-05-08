import abc
from collections import namedtuple

import numpy as np


class Solver(abc.ABC):

    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    @abc.abstractmethod
    def solve(self, state_initial):
        pass


class Newton(Solver):

    def solve(self):
        system = self.manager.system
        time_stepper = self.manager.time_stepper

        system.initialize()
        states = system.states

        #  time-stepping
        time = time_stepper.start

        time_index = 0
        while time < time_stepper.end:
            print(f"time={time}")
            states.time[time_index] = time
            states.state_n = states.state_n1

            states.state_n1 = self.newton_update()
            states.state[time_index + 1, :] = states.state_n1

            time = time + time_stepper.stepsize
            time_index = time_index + 1

        return states

    def newton_update(self):
        states = self.manager.system.states

        residual_norm = 1e5
        index_iteration = 0
        while (residual_norm >= self.newton_epsilon) and (
            index_iteration < self.max_iterations
        ):
            index_iteration += 1
            residual, tangent_matrix = self.manager.integrator.calc_residuum_tangent()
            state_delta = -np.linalg.inv(tangent_matrix) @ residual
            states.state_n1 = states.state_n1 + state_delta
            residual_norm = np.linalg.norm(residual)

        return states.state_n1
