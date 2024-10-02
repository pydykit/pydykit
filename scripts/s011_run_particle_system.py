import plotly.graph_objects as go

import pydykit

name = "particle_system_01"
# name = "particle_system_02"

manager = pydykit.managers.Manager()

path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)
result = manager.manage()

tmp = manager.system.internal_potential()
print(tmp)

df = result.to_df()
fig = go.Figure()

for index in range(manager.system.nbr_particles):
    index = pydykit.utils.shift_index_python_to_literature(index)

    pydykit.plotting.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"x{index}"],
        y_components=df[f"y{index}"],
        z_components=df[f"z{index}"],
        time=df["time"],
    )

    index_time = 0
    pydykit.plotting.add_3d_annotation(
        figure=fig,
        x=df[f"x{index}"][index_time],
        y=df[f"y{index}"][index_time],
        z=df[f"z{index}"][index_time],
        text=str(index),
    )


fig.update_layout(font_family="Serif")

pydykit.plotting.fix_scene_bounds_to_extrema(figure=fig, df=df)

fig.show()

df.to_csv(f"test/reference_results/{name}.csv")
