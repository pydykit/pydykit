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


def get_extremum_position_value_over_all_particles(
    df,
    axis="x",
    extremum="max",
):
    tmp = df.filter(
        regex=f"^[{axis}][\d]$",
        axis=1,
    )
    tmp = getattr(tmp, extremum)(numeric_only=True)
    tmp = getattr(tmp, extremum)()
    return tmp


def fix_scene_bounds_to_extrema(
    figure,
    df,
    aspectmode="data",
):
    figure.update_layout(
        scene=dict(
            {
                f"{axis}axis": dict(
                    range=[
                        get_extremum_position_value_over_all_particles(
                            df=df,
                            axis=axis,
                            extremum="min",
                        ),
                        get_extremum_position_value_over_all_particles(
                            df=df,
                            axis=axis,
                            extremum="max",
                        ),
                    ],
                    autorange=False,
                )
                for axis in ["x", "y", "z"]
            },
            # xaxis=dict(autorange=True),
            # yaxis=dict(autorange=True),
            # zaxis=dict(autorange=True),
            aspectmode=aspectmode,
        )
    )
