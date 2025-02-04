import re

import plotly.graph_objects as go


class Plotter:

    def __init__(self, results_df):

        self.results_df = results_df
        self.plotting_backend = "plotly"
        self.color_palette = [
            "#0072B2",
            "#009E73",
            "#D55E00",
            "#56B4E9",
            "#CC79A7",
            "#E69F00",
            "#F0E442",
        ]
        # color scheme (color-blind friendly)
        # https://clauswilke.com/dataviz/color-pitfalls.html#not-designing-for-color-vision-deficiency

    def plot_3d_trajectory(self, figure, **kwargs):

        figure.add_trace(self.get_trace_3d_trajectory(**kwargs))

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_extremum_position_value_over_all_particles(
        df,
        axis="x",
        extremum="max",
    ):
        tmp = df.filter(
            regex=rf"^[{axis}][\d]$",
            axis=1,
        )
        tmp = getattr(tmp, extremum)(numeric_only=True)
        tmp = getattr(tmp, extremum)()
        return tmp

    def fix_scene_bounds_to_extrema(
        self,
        figure,
        df,
        aspectmode="data",
    ):

        figure.update_layout(
            scene=dict(
                {
                    f"{axis}axis": dict(
                        range=[
                            self.get_extremum_position_value_over_all_particles(
                                df=df,
                                axis=axis,
                                extremum="min",
                            ),
                            self.get_extremum_position_value_over_all_particles(
                                df=df,
                                axis=axis,
                                extremum="max",
                            ),
                        ],
                        autorange=False,
                    )
                    for axis in ["x", "y", "z"]
                },
                aspectmode=aspectmode,
            )
        )

    def visualize_time_evolution(
        self,
        quantities,
        y_axis_label="value",
        y_axis_scale="linear",
        figure: None | go.Figure = None,
    ):

        pd.options.plotting.backend = self.plotting_backend

        columns_to_plot = []
        for quantity in quantities:
            columns_to_plot = utils.add_columns_to_plot(
                columns_to_plot, self.results_df, quantity
            )

        fig = self.plot_time_evolution(
            quantities=columns_to_plot,
            y_axis_label=y_axis_label,
            y_axis_scale=y_axis_scale,
        )

        if figure is None:
            # Start from new figure
            figure = fig
        else:
            # Enrich existing figure
            figure.add_traces(list(fig.select_traces()))

        return figure

    def plot_time_evolution(self, quantities, y_axis_label, y_axis_scale):

        fig = go.Figure()

        # Loop through each quantity to create a separate trace
        for quantity in quantities:
            fig.add_trace(
                go.Scatter(
                    x=self.results_df["time"],
                    y=self.results_df[quantity],
                    mode="lines",
                    name=quantity,  # Label for the legend
                )
            )

        # Update layout to include labels and colors
        fig.update_layout(
            xaxis_title="time",
            yaxis_title=y_axis_label,
            colorway=self.color_palette,
        )

        # Adapt scaling
        fig.update_layout(yaxis_type=y_axis_scale)
        return fig
