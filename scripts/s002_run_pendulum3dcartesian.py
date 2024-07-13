import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pymetis
import pathlib

# get absolute config file path
current_parent_path = pathlib.Path(__file__).parent.resolve()
relative_config_file_path = "../pymetis/example_files/pendulum3dcartesian.yml"
absolute_config_file_path = (current_parent_path / relative_config_file_path).resolve()

manager = pymetis.Manager(path_config_file=absolute_config_file_path)
result = manager.manage()

print("Success, start plotting")

df = result.to_df()
# df.to_csv("test/reference_results/pendulum3dcartesian.csv")

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
