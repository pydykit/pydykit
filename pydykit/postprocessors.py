import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import utils


class Postprocessor:

    def __init__(self, manager, results_df: pd.DataFrame):

        self.manager = manager
        self.results_df = results_df
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
        self.nbr_time_point = len(self.results_df)

        for quantity in self.quantities:
            # Determine function dimensions and initialize data
            system_function = getattr(system, quantity)
            dim_function = system_function().ndim
            data = self.create_zeros_array(
                dimension_x=self.nbr_time_point, dimension_y=dim_function
            )

            # Evaluate and collect data for each time point
            for step_index in range(self.nbr_time_point):
                system = self.update_system(system, step_index)
                data[step_index] = getattr(system, quantity)()

            # Append the new data to the results DataFrame
            self.results_df[quantity] = data

    def create_zeros_array(self, dimension_x, dimension_y):
        if dimension_y == 0:
            return np.zeros(dimension_x)
        else:
            return np.zeros((dimension_x, dimension_y))

    def update_system(self, system, index):
        updated_state = utils.row_array_from_df(df=self.results_df, index=index)
        system = system.copy(state=updated_state)
        return system

    def visualize(
        self,
        quantities=None,
        y_axis_label="value",
        figure: None | go.Figure = None,
    ):

        # Sometimes we want to plot existing state, e.g., position or momentum
        if quantities is None:
            # By default, plot all explicitly calculated quantities
            quantities = self.quantities

        pd.options.plotting.backend = self.plotting_backend

        fig = self.plot_single_figure(
            quantities=quantities,
            y_axis_label=y_axis_label,
        )
        # I like to show explicitly...
        # fig.show()

        # Sometimes we want to enrich existing figures
        if figure is None:
            figure = fig
        else:
            figure.add_traces(list(fig.select_traces()))

        # Passing figures is convenient
        return figure

    def plot_single_figure(self, quantities, y_axis_label):
        # TODO: IF we switch to using plotly.graphobjects (go), we will be better of... instead of adding figures, we would then add traces.
        return self.results_df.plot(
            x="time",
            y=quantities,  # I did not like the loop approach
            labels={
                "index": "time",
                "value": y_axis_label,
            },
            color_discrete_sequence=self.color_palette,
        )
