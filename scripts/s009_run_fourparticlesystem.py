import os

import plotly.graph_objects as go
import tikzplotly

import pydykit

manager = pydykit.managers.Manager()
name = "four_particle_system"
path_config_file = f"./pydykit/example_files/{name}.yml"
manager.configure_from_path(path=path_config_file)
result = manager.manage()

df = result.to_df()
fig = go.Figure()

pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["x1"],
    y_components=df["y1"],
    z_components=df["z1"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["x2"],
    y_components=df["y2"],
    z_components=df["z2"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["x3"],
    y_components=df["y3"],
    z_components=df["z3"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["x4"],
    y_components=df["y4"],
    z_components=df["z4"],
    time=df["time"],
)

fig.update_layout(font_family="Serif")

fig.show()
