import matplotlib.pyplot as plt
import numpy as np
import pymetis

manager = pymetis.Manager(path_config_file="./pymetis/example_files/pendulum.yml")
result = manager.manage()


print(result)


fig, ax = plt.subplots()

ax.plot(
    result.time[:],
    result.state[:, 0],
    marker="x",
)
ax.plot(
    result.time[:],
    result.state[:, 1],
    marker="x",
)

plt.show()
