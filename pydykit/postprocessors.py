import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import utils


class Postprocessor:

    def __init__(
        self,
        manager,
        state_results_df: pd.DataFrame,
        postprocessed_data_from_integrator: list = None,
    ):

        self.manager = manager
        self.postprocessed_data_from_integrator = postprocessed_data_from_integrator
        self.results_df = state_results_df
        self.quantities = []
        self.evaluation_points = []
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
        self.evaluation_strategy_factory = EvaluationStrategyFactory(self)

    @property
    def state_results_df(self):
        return self.results_df[self.manager.system.state_columns]

    @property
    def available_evaluation_points(self):
        return list(self._evaluation_strategies.keys())

    def postprocess(
        self, quantities, evaluation_points, weighted_by_timestepsize=False
    ):

        self.quantities += quantities
        self.evaluation_points += evaluation_points

        system = self.manager.system
        self.nbr_time_point = self.manager.time_stepper.nbr_time_points

        invalid_points = set(evaluation_points) - set(
            self.evaluation_strategy_factory.available_evaluation_points()
        )

        if invalid_points:
            raise utils.PydykitException(
                f"Invalid evaluation points: {', '.join(invalid_points)}"
            )

        for index, quantity in enumerate(quantities):

            # Get the appropriate evaluation strategy
            eval_point = evaluation_points[index]

            if hasattr(system, quantity):

                # Determine function dimensions and initialize data
                system_function = getattr(system, quantity)
                dim_function = system_function().ndim
                data = np.zeros([self.nbr_time_point, dim_function + 1])

                # Evaluate and collect data for each time point
                for step_index in range(self.nbr_time_point):
                    strategy = self.evaluation_strategy_factory.get_strategy(
                        eval_point=eval_point
                    )
                    data[step_index] = strategy(
                        system=system, quantity=quantity, step_index=step_index
                    )
            elif quantity in self.postprocessed_data_from_integrator[0]:
                dim_function = self.postprocessed_data_from_integrator[0][quantity].ndim
                data = np.zeros([self.nbr_time_point, dim_function + 1])
                for step_index in range(self.nbr_time_point):
                    if not step_index + 1 == self.nbr_time_point:
                        data[step_index] = self.postprocessed_data_from_integrator[
                            step_index
                        ][quantity]
            else:
                raise utils.PydykitException(
                    f"{quantity} is not suitable for postprocessing since its not a method of {system} and not contained in {self.postprocessed_data_from_integrator}"
                )

            if weighted_by_timestepsize:
                data = data * self.manager.time_stepper.current_step.increment

            # Handle DataFrame column naming and assignment
            self._assign_to_dataframe(
                data=data,
                quantity=quantity,
                dim_function=dim_function,
                eval_point=eval_point,
            )

    def _evaluate_current_time(self, system, quantity, step_index):
        system_current_time = self.update_system(system=system, index=step_index)
        return getattr(system_current_time, quantity)()

    def _evaluate_interval_midpoint(self, system, quantity, step_index):
        if step_index + 1 == self.nbr_time_point:
            return np.nan

        system_current_time = self.update_system(system=system, index=step_index)
        system_next_time = self.update_system(system=system, index=step_index + 1)
        state_midpoint = 0.5 * (system_current_time.state + system_next_time.state)

        system_current_time, system_midpoint = (
            utils.get_system_copies_with_desired_states(
                system=self.manager.system,
                states=[system_current_time.state, state_midpoint],
            )
        )
        return getattr(system_midpoint, quantity)()

    def _evaluate_interval_increment(self, system, quantity, step_index):
        if step_index + 1 == self.nbr_time_point:
            return np.nan

        system_current_time = self.update_system(system=system, index=step_index)
        system_next_time = self.update_system(system=system, index=step_index + 1)
        return (
            getattr(system_next_time, quantity)()
            - getattr(system_current_time, quantity)()
        )

    def _assign_to_dataframe(self, data, quantity, dim_function, eval_point):
        if dim_function == 0:
            column = f"{quantity}_{eval_point}"
            self.results_df[column] = data.squeeze()
        else:
            column = [(f"{quantity}_{eval_point}_{i}") for i in range(dim_function + 1)]
            self.results_df[column] = data

    def update_system(self, system, index):
        updated_state = utils.row_array_from_df(df=self.state_results_df, index=index)
        return system.copy(state=updated_state)

    def visualize(
        self,
        quantities=None,
        y_axis_label="value",
        y_axis_scale="linear",
        figure: None | go.Figure = None,
    ):

        if quantities is None:
            # By default, plot all explicitly calculated quantities
            quantities = self.quantities

        pd.options.plotting.backend = self.plotting_backend

        columns_to_plot = []
        for quantity in quantities:
            columns_to_plot += [
                col
                for col in self.results_df.columns
                if re.search(rf"^{quantity}(_\d+)?$", col)
            ]

        fig = self.plot_single_figure(
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

    def plot_single_figure(self, quantities, y_axis_label, y_axis_scale):

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

    def add_sum_of(self, quantities, sum_name):
        self.results_df[sum_name] = self.results_df[quantities].sum(
            axis=1, skipna=False
        )

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
            regex=f"^[{axis}][\d]$",
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


class EvaluationStrategyFactory:
    def __init__(self, postprocessor):
        self.postprocessor = postprocessor
        self.strategies = {
            "current_time": self.postprocessor._evaluate_current_time,
            "interval_midpoint": self.postprocessor._evaluate_interval_midpoint,
            "interval_increment": self.postprocessor._evaluate_interval_increment,
        }

    def get_strategy(self, eval_point):
        return self.strategies[eval_point]

    def available_evaluation_points(self):
        return self.strategies.keys()
