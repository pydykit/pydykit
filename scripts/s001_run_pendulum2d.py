import matplotlib.pyplot as plt
import numpy as np
import pymetis

manager = pymetis.Manager(path_config_file="./pymetis/example_files/pendulum2d.yml")
result = manager.manage()
df = result.to_df(
    indices=[0, 1],
    columns=["x", "y"],
)

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
