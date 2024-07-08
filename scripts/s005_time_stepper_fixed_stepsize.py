import numpy as np
from pymetis import time_steppers

stepper = time_steppers.FixedIncrement(
    start=1,
    end=2.2,
    stepsize=0.15,
    manager=None,
)

print(stepper.times)

from itertools import pairwise

increments = np.array([n1 - n for n, n1 in pairwise(stepper.times)])

increments_equal_stepsize = np.isclose(increments, stepper.stepsize)

print(increments_equal_stepsize)

assert all(
    increments_equal_stepsize
), "Please choose arguments of FixedIncrement such that increments are homogeneous"
