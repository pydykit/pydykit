import plotly.graph_objects as go


def plot_3d_trajectory(figure, **kwargs):
    figure.add_trace(get_trace_3d_trajectory(**kwargs))


def get_trace_3d_trajectory(
    x_components,
    y_components,
    z_components,
    time,
):
    return go.Scatter3d(
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


def add_3d_annotation(
    figure,
    text,
    x,
    y,
    z,
    ax=35,
    ay=0,
    xanchor="center",
    yanchor="bottom",
    arrowhead=1,
):

    new = dict(
        x=x,
        y=y,
        z=z,
        text=text,
        ax=ax,
        ay=ay,
        xanchor=xanchor,
        yanchor=yanchor,
        arrowhead=arrowhead,
    )

    existing = list(figure.layout.scene.annotations)

    annotations = existing + [
        new,
    ]

    figure.update_layout(
        scene=dict(annotations=annotations),
    )
