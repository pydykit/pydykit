import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import utils


class Postprocessor:

    def __init__(self, manager, state_results_df: pd.DataFrame):

        self.manager = manager
        self.results_df = state_results_df
        self.quantities = []
        self.evaluation_points = []
        self.color_palette = [
            "#0072B2",
            "#009E73",
            "#D55E00",
            "#56B4E9",
            "#CC79A7",
            "#E69F00",
            "#F0E442",
        ]
        self.plotting_backend = "plotly"
        # color scheme (color-blind friendly)
        # https://clauswilke.com/dataviz/color-pitfalls.html#not-designing-for-color-vision-deficiency

    @property
    def state_results_df(self):
        return self.results_df[self.manager.system.state_columns]

    def postprocess(
        self, quantities, evaluation_points, weighted_by_timestepsize=False
    ):

        self.quantities += quantities
        self.evaluation_points += evaluation_points

        system = self.manager.system
        self.nbr_time_point = self.manager.time_stepper.nbr_time_points

        for index, quantity in enumerate(quantities):
            # Determine function dimensions and initialize data
            system_function = getattr(system, quantity)
            dim_function = system_function().ndim
            data = np.zeros([self.nbr_time_point, dim_function + 1])

            # Evaluate and collect data for each time point
            for step_index in range(self.nbr_time_point):
                system_n = self.update_system(system, step_index)
                if not step_index + 1 == self.nbr_time_point:
                    system_n1 = self.update_system(system, step_index + 1)

                if evaluation_points[index] == "n":
                    data[step_index] = getattr(system_n, quantity)()
                elif (
                    evaluation_points[index] == "n05"
                    and not step_index + 1 == self.nbr_time_point
                ):
                    state_n = system_n.state
                    state_n1 = system_n1.state
                    state_n05 = 0.5 * (state_n + state_n1)
                    system_n, system_n05 = utils.get_system_copies_with_desired_states(
                        system=self.manager.system,
                        states=[
                            state_n,
                            state_n05,
                        ],
                    )
                    data[step_index] = getattr(system_n05, quantity)()
                elif (
                    evaluation_points[index] == "n1-n"
                    and not step_index + 1 == self.nbr_time_point
                ):
                    data[step_index] = (
                        getattr(system_n1, quantity)() - getattr(system_n, quantity)()
                    )
                elif (
                    evaluation_points[index] == "n1-n"
                    and step_index + 1 == self.nbr_time_point
                ) or (
                    evaluation_points[index] == "n05"
                    and step_index + 1 == self.nbr_time_point
                ):
                    data[step_index] = np.nan
                else:
                    raise utils.PydykitException(
                        f"Evaluation point choice {evaluation_points[index]} not implemented."
                    )

            if weighted_by_timestepsize:
                data = data * self.manager.time_stepper.current_step.increment

            if dim_function == 0:
                column = (
                    quantity
                    if not self.evaluation_points[index] == "n1-n"
                    else f"{quantity}_difference"
                )

                self.results_df[column] = data.squeeze()
            else:
                column = [
                    (
                        f"{quantity}_{i}"
                        if not self.evaluation_points[index] == "n1-n"
                        else f"{quantity}_{i}_difference"
                    )
                    for i in range(dim_function + 1)
                ]
                # Append the new data to the results DataFrame
                self.results_df[column] = data

    def update_system(self, system, index):
        updated_state = utils.row_array_from_df(df=self.state_results_df, index=index)
        system = system.copy(state=updated_state)
        return system

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
        # TODO: IF we switch to using plotly.graphobjects (go), we will be better of.
        #       Instead of adding figures, we would then add traces.

        fig = self.results_df.plot(
            x="time",
            y=quantities,
            labels={
                "index": "time",
                "value": y_axis_label,
            },
            color_discrete_sequence=self.color_palette,
        )
        fig.update_layout(yaxis_type=y_axis_scale)
        return fig

    def add_sum_of(self, quantities, sum_name):
        self.results_df[sum_name] = self.results_df[quantities].sum(
            axis=1, skipna=False
        )
