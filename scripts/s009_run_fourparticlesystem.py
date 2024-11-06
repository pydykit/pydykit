import os

import plotly.graph_objects as go
import tikzplotly

import pydykit

manager = pydykit.managers.Manager()
name = "four_particle_system_discrete_gradient"
path_config_file = f"./pydykit/example_files/{name}.yml"
manager.configure_from_path(path=path_config_file)
result = manager.manage()

df = result.to_df()
fig = go.Figure()
for index in range(manager.system.nbr_particles):
    pydykit.plotting.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position0_particle{index}"],
        y_components=df[f"position1_particle{index}"],
        z_components=df[f"position2_particle{index}"],
        time=df["time"],
    )

fig.update_layout(font_family="Serif")

fig.show()

# df.to_csv(f"test/reference_results/{name}.csv")
