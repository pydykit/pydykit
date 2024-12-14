import plotly.graph_objects as go

import pydykit
import pydykit.postprocessors as postprocessors

# name = "particle_system_02"
name = "particle_system_03"
# name = "pendulum_3d_cartesian"

manager = pydykit.managers.Manager()

path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)
result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)


df = result.to_df()
fig = go.Figure()

postprocessor = postprocessors.Postprocessor(manager, state_results_df=df)


for index in range(manager.system.nbr_particles):

    postprocessor.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position0_particle{index}"],
        y_components=df[f"position1_particle{index}"],
        z_components=df[f"position2_particle{index}"],
        time=df["time"],
    )

    index_time = 0
    postprocessor.add_3d_annotation(
        figure=fig,
        x=df[f"position0_particle{index}"][index_time],
        y=df[f"position1_particle{index}"][index_time],
        z=df[f"position2_particle{index}"][index_time],
        text=str(index),
    )


fig.update_layout(font_family="Serif")

postprocessor.fix_scene_bounds_to_extrema(figure=fig, df=df)

fig.show()

# df.to_csv(f"test/reference_results/{name}.csv")
