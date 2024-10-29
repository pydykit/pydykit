import numpy as np

from pydykit import time_steppers

# stepper = time_steppers.FixedIncrementKinon(
#     start=1.0,
#     end=2.2,
#     step_size=0.15,
#     manager=None,
# )

stepper = time_steppers.FixedIncrement(
    start=1.0,
    end=2.2,
    step_size=0.1,
    manager=None,
)

print(stepper.times)

from itertools import pairwise

increments = np.array([n1 - n for n, n1 in pairwise(stepper.times)])

increments_equal_step_size = np.isclose(increments, stepper.step_size)
print(increments)
print(increments_equal_step_size)

assert all(
    increments_equal_step_size
), "Please choose arguments of FixedIncrement such that increments are homogeneous"
