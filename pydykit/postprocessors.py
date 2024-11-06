import numpy as np
import pandas as pd

from . import utils


class Postprocessor:

    def __init__(self, manager, results_df, quantities):

        self.manager = manager
        self.results_df = results_df
        self.quantities = quantities
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

    def postprocess(self):
        system = self.manager.system
        self.nbr_time_point = len(self.results_df)

        for quantity in self.quantities:
            system_function = getattr(system, quantity)
            dim_function = system_function().ndim
            # create empty df
            if dim_function == 0:
                data = np.zeros(self.nbr_time_point)
            else:
                data = np.zeros(self.nbr_time_point, dim_function)

            for step_index in range(self.nbr_time_point):
                # update state and system
                system.state = utils.row_array_from_df(
                    df=self.results_df, index=step_index
                )
                system_function = getattr(system, quantity)
                # evaluate function
                data[step_index] = system_function()

            # write row of daraframe
            new_df = pd.DataFrame({quantity: data})
            self.results_df = pd.concat([self.results_df, new_df], axis=1)

    def visualize(self):
        pd.options.plotting.backend = self.plotting_backend

        for quantity in self.quantities:
            x_value_identifier = "time"
            y_value_identifiers = quantity
            fig = self.results_df.plot(
                x=x_value_identifier,
                y=y_value_identifiers,
                labels=dict(index=x_value_identifier, value=quantity),
                color_discrete_sequence=self.color_palette,
            )
            fig.show()
