import pydykit
import plotly.graph_objects as go


manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/fourparticlesystem.yml"
)

result = manager.manage()

df = result.to_df()

fig = go.Figure(
    data=go.Scatter3d(
        x=df["x1"],
        y=df["y1"],
        z=df["z1"],
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

fig.add_trace(
    go.Scatter3d(
        x=df["x2"],
        y=df["y2"],
        z=df["z2"],
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

fig.add_trace(
    go.Scatter3d(
        x=df["x3"],
        y=df["y3"],
        z=df["z3"],
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

fig.add_trace(
    go.Scatter3d(
        x=df["x4"],
        y=df["y4"],
        z=df["z4"],
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
