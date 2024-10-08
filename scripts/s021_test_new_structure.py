import plotly.graph_objects as go

import pydykit

# instantiate manager
manager = pydykit.managers.Manager()

# configure manager from input
name = "pendulum_3d_cartesian"
path_config_file = f"./pydykit/example_files/{name}.yml"
manager.configure_from_path(path=path_config_file)

# run simulation and store to dataframe
result = manager.manage()
df = result.to_df()

# postprocess
fig = go.Figure(
    data=go.Scatter3d(
        x=df["position1"],
        y=df["position2"],
        z=df["position3"],
        marker=dict(
            size=3,
            color=df["time"],
            colorscale="Viridis",
            colorbar=dict(
                thickness=20,
                title="time",
            ),
        ),
        line=dict(
            color="darkblue",
            width=3,
        ),
    )
)

fig.show()
