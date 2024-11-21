import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import utils


class Postprocessor:

    def __init__(self, manager, state_results_df: pd.DataFrame):

        self.manager = manager
        self.state_results_df = state_results_df
        self.post_results_df = pd.DataFrame()
        self.results_df = pd.DataFrame()
        self.quantities = []
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

    def postprocess(self, quantities):

        self.quantities += quantities

        system = self.manager.system
        self.nbr_time_point = len(self.state_results_df)

        for quantity in self.quantities:
            # Determine function dimensions and initialize data
            system_function = getattr(system, quantity)
            dim_function = system_function().ndim
            data = np.zeros([self.nbr_time_point, dim_function + 1])

            # Evaluate and collect data for each time point
            for step_index in range(self.nbr_time_point):
                system = self.update_system(system, step_index)
                data[step_index] = getattr(system, quantity)()

            if dim_function == 0:
                self.post_results_df[quantity] = data.squeeze()
            else:
                column = [f"{quantity}_{i}" for i in range(dim_function + 1)]
                # Append the new data to the results DataFrame
                self.post_results_df[column] = data

        self.results_df = pd.concat(
            [self.state_results_df, self.post_results_df], axis=1
        )

        0

    def update_system(self, system, index):
        updated_state = utils.row_array_from_df(df=self.state_results_df, index=index)
        system = system.copy(state=updated_state)
        return system

    def visualize(
        self,
        quantities=None,
        y_axis_label="value",
        figure: None | go.Figure = None,
    ):

        if quantities is None:
            # By default, plot all explicitly calculated quantities
            quantities = self.quantities

        pd.options.plotting.backend = self.plotting_backend

        columns_to_plot = [
            col
            for col in self.results_df.columns
            if re.search(rf"^{quantities}(_\d+)?$", col)
        ]

        fig = self.plot_single_figure(
            quantities=columns_to_plot,
            y_axis_label=y_axis_label,
        )

        if figure is None:
            # Start from new figure
            figure = fig
        else:
            # Enrich existing figure
            figure.add_traces(list(fig.select_traces()))

        return figure

    def plot_single_figure(self, quantities, y_axis_label):
        # TODO: IF we switch to using plotly.graphobjects (go), we will be better of.
        #       Instead of adding figures, we would then add traces.

        return self.results_df.plot(
            x="time",
            y=quantities,
            labels={
                "index": "time",
                "value": y_axis_label,
            },
            color_discrete_sequence=self.color_palette,
        )
