import os

import plotly.graph_objects as go
import tikzplotly

import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/particle_system.yml"
)

result = manager.manage()

q, p, lambd = manager.system.decompose_state(manager.system.states.state_n)
tmp = manager.system.internal_potential(q=q)
print(tmp)

df = result.to_df()
fig = go.Figure()

pydykit.utils.plot_three_dimensional_trajectory(
    figure=fig,
    x_components=df["x1"],
    y_components=df["y1"],
    z_components=df["z1"],
    time=df["time"],
)
pydykit.utils.plot_three_dimensional_trajectory(
    figure=fig,
    x_components=df["x2"],
    y_components=df["y2"],
    z_components=df["z2"],
    time=df["time"],
)
pydykit.utils.plot_three_dimensional_trajectory(
    figure=fig,
    x_components=df["x3"],
    y_components=df["y3"],
    z_components=df["z3"],
    time=df["time"],
)
pydykit.utils.plot_three_dimensional_trajectory(
    figure=fig,
    x_components=df["x4"],
    y_components=df["y4"],
    z_components=df["z4"],
    time=df["time"],
)

fig.update_layout(font_family="Serif")

fig.show()
