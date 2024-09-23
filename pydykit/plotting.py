import plotly.graph_objects as go


def plot_3d_trajectory(
    figure,
    x_components,
    y_components,
    z_components,
    time,
):
    figure.add_trace(
        go.Scatter3d(
            x=x_components,
            y=y_components,
            z=z_components,
            marker=dict(
                size=3,
                color=time,
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
            showlegend=False,
        )
    )
