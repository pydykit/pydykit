import plotly.graph_objects as go

import pydykit

# name = "particle_system_02"
name = "particle_system_03"
# name = "pendulum_3d_cartesian"

manager = pydykit.managers.Manager()

path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)
result = manager.manage()

tmp = manager.system.internal_potential()
print(tmp)

df = result.to_df()
fig = go.Figure()

for index in range(manager.system.nbr_particles):
    index = index + 1

    pydykit.plotting.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position_x{index}"],
        y_components=df[f"position_y{index}"],
        z_components=df[f"position_z{index}"],
        time=df["time"],
    )

    index_time = 0
    pydykit.plotting.add_3d_annotation(
        figure=fig,
        x=df[f"position_x{index}"][index_time],
        y=df[f"position_y{index}"][index_time],
        z=df[f"position_z{index}"][index_time],
        text=str(index),
    )


fig.update_layout(font_family="Serif")

pydykit.plotting.fix_scene_bounds_to_extrema(figure=fig, df=df)

fig.show()

df.to_csv(f"test/reference_results/{name}.csv")
