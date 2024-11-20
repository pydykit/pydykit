import matplotlib.pyplot as plt
import numpy as np

import pydykit

manager = pydykit.managers.Manager()

name = "pendulum_2d"
path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)

result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)
df = result.to_df()

print(result)


fig, ax = plt.subplots()

ax.plot(
    result.times[:],
    result.results[:, 0],
    marker="x",
)
ax.plot(
    result.times[:],
    result.results[:, 1],
    marker="x",
)

plt.show()
