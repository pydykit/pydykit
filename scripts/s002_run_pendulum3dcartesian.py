import pathlib

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import pydykit

manager = pydykit.managers.Manager()

name = "pendulum_3d_cartesian"
path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)

result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)
df = result.to_df()

# df.to_csv("test/reference_results/pendulum_3d_cartesian.csv")

fig = go.Figure(
    data=go.Scatter3d(
        x=df["position0_particle0"],
        y=df["position1_particle0"],
        z=df["position2_particle0"],
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
