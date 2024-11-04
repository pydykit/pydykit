import plotly.graph_objects as go

import pydykit

container = pydykit.containers.Container()

name = "reactor"
path_config_file = f"./pydykit/example_files/{name}.yml"

file_content = pydykit.utils.load_yaml_file(
    path=path_config_file,
)
configuration = pydykit.configurations.Configuration(
    **file_content["configuration"],
)

container.config = configuration

container.wire(modules=[__name__])

manager = (
    pydykit.managers.Manager
)  # <-- inject dependency on configuration, system, simulator, integrator, time_stepper and result here

result = manager.manage()
df = result.to_df()

fig = go.Figure()
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["concentration"],
    y_components=df["temperature"],
    z_components=df["reaction_rate"],
    time=df["time"],
)

fig.update_layout(font_family="Serif")

fig.show()

# df.to_csv(f"test/reference_results/{name}.csv")
