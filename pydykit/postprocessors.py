import inspect

import pandas as pd

import pydykit

from . import base_classes, utils


class Postprocessor:

    def __init__(self, manager, path_config_file=None, content_config_file=None):

        utils.update_object_from_config_file(
            self, path_config_file, content_config_file
        )

        for quantity in self.configuration["quantity_names"]:
            quantity_instance = globals()[quantity]()
            setattr(self, quantity, quantity_instance)

        self.manager = manager
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

    def postprocess(self, df):
        system = self.manager.system
        self.nbr_time_point = len(df)

        for quantity in self.configuration["quantity_names"]:
            quantity_instance = getattr(self, quantity)
            quantity_instance.create_dataframe(nbr_time_point=self.nbr_time_point)

        for step_index in range(self.nbr_time_point):
            state = pydykit.states.State.from_df(df, step_index)
            q, p, lambd = system.decompose_state(state)

            for quantity in self.configuration["quantity_names"]:
                function_list = globals()[quantity]().functions
                quantity_instance = getattr(self, quantity)
                for function in function_list:
                    system_function = getattr(system, function)
                    input_dict = self.determine_args_dict(system_function, q, p, lambd)
                    # if quantity_instance.
                    quantity_instance.df.at[step_index, function] = system_function(
                        **input_dict
                    )

        # merg dataframe
        for quantity in self.configuration["quantity_names"]:
            quantity_instance = getattr(self, quantity)
            df = pd.concat([df, quantity_instance.df], axis=1)

        return df

    def visualize(self, df):
        pd.options.plotting.backend = "plotly"

        for quantity in self.configuration["quantity_names"]:
            fig = self.create_line_plot(quantity, df)
            fig.show()

    def create_line_plot(self, quantity, df):
        quantity_instance = getattr(self, quantity)
        x_value_identifier = "time"
        y_value_identifiers = quantity_instance.functions
        fig = df.plot(
            x=x_value_identifier,
            y=y_value_identifiers,
            labels=dict(index=x_value_identifier, value=quantity),
            color_discrete_sequence=self.color_palette,
        )
        return fig

    @staticmethod
    def determine_args_dict(function, q, p, lambd):
        args_list = inspect.getfullargspec(function)[0]
        args_list.remove("self")
        if args_list == ["q", "p"]:
            z = [q, p]
        elif args_list == ["q"]:
            z = [q]
        elif args_list == ["p"]:
            z = [p]
        else:
            raise Exception("Not implemented")

        return dict(zip(args_list, z))


class Energy(base_classes.Quantity):
    def __init__(self):
        super().__init__()
        self.dimension = [1, 1, 1]
        self.functions = [
            "kinetic_energy",
            "potential_energy",
            "total_energy",
        ]


class Constraint(base_classes.Quantity):
    def __init__(self):
        super().__init__()
        self.dimension = [1]
        self.functions = ["constraint"]


class Constraint_Velocity(base_classes.Quantity):
    def __init__(self):
        super().__init__()
        self.dimension = [1]
        self.functions = ["constraint_velocity"]


class Angular_Momentum(base_classes.Quantity):
    def __init__(self):
        super().__init__()
        self.dimension = [3]
        self.functions = ["angular_momentum"]
