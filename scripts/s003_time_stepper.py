from pydykit import time_steppers


def print_time_step(time_step):
    print(
        time_step.index,
        time_step.time,
        time_step.increment,
    )


stepper = time_steppers.FixedIncrementHittingEnd(
    start=1,
    end=2.2,
    step_size=0.15,
    manager=None,
)

print(stepper.times)


for time_step in stepper.make_steps():
    print_time_step(time_step)

print("#########")


steps = stepper.make_steps()

time_step = next(steps)
print_time_step(time_step)

for time_step in steps:
    print_time_step(time_step)


from itertools import chain, islice, tee


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


for previous, item, nxt in previous_and_next(stepper.times):
    print("Item is now", item, "next is", nxt, "previous is", previous)

# Literature
# https://realpython.com/introduction-to-python-generators/
# https://stackoverflow.com/questions/1011938/loop-that-also-accesses-previous-and-next-values
