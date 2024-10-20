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
    x_components=df["position_x0"],
    y_components=df["position_y0"],
    z_components=df["position_z0"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position_x1"],
    y_components=df["position_y1"],
    z_components=df["position_z1"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position_x2"],
    y_components=df["position_y2"],
    z_components=df["position_z2"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position_x3"],
    y_components=df["position_y3"],
    z_components=df["position_z3"],
    time=df["time"],
)

fig.update_layout(font_family="Serif")

fig.show()
