import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymetis

manager = pymetis.Manager(
    path_config_file="./pymetis/example_files/pendulum3dcartesian.yml"
)
result = manager.manage()


print(result)


import numpy as np
import plotly.express as px
import plotly.graph_objects as go

x, y, z = result.state[:, 0], result.state[:, 1], result.state[:, 2]

df = pd.DataFrame(data=result.state[:, [0, 1, 2]], columns=["x", "y", "z"])
df["time"] = result.time

# fig = px.line_3d(
#     df,
#     x="x",
#     y="y",
#     z="z",
#     color="time",
# )


fig = go.Figure(
    data=go.Scatter3d(
        x=df["x"],
        y=df["y"],
        z=df["z"],
        marker=dict(
            size=3,
            color=df["time"],
            colorscale="Viridis",
            colorbar=dict(
                thickness=20,
                title="time",
            ),
        ),
        line=dict(
            color="darkblue",
            width=3,
        ),
    )
)

fig.show()
