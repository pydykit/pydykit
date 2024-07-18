import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/pendulum3dcartesian_full_time.yml"
)
result = manager.manage()

print("Success, start plotting")

df = result.to_df()
df.to_csv("test/reference_results/pendulum3dcartesian_full_time.csv")

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
