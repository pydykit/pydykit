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
    x_components=df["position1"],
    y_components=df["position2"],
    z_components=df["position3"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position4"],
    y_components=df["position5"],
    z_components=df["position6"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position7"],
    y_components=df["position8"],
    z_components=df["position9"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position10"],
    y_components=df["position11"],
    z_components=df["position12"],
    time=df["time"],
)

fig.update_layout(font_family="Serif")

fig.show()
