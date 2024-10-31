import plotly.graph_objects as go

import pydykit
import pydykit.containers
import pydykit.factories as factories

container = pydykit.containers.Container()
manager = container.manager_factory()

name = "reactor"
path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)
manager.result = factories.result_factory.get(
    key="Result",
)
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
