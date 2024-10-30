import plotly.graph_objects as go

import pydykit

manager = pydykit.managers.Manager()

name = "reactor"
path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)

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
