import abc
import copy
import importlib
import inspect

import numpy as np
import pandas as pd

import pydykit

from . import utils


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
                    quantity_instance.df.at[step_index, function] = system_function(
                        **input_dict
                    )

        # merg dataframe
        for quantity in self.configuration["quantity_names"]:
            quantity_instance = getattr(self, quantity)
            df = pd.concat([df, quantity_instance.df], axis=1)

        return df

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


class Quantity(abc.ABC):

    def __init__(self):
        pass

    def create_dataframe(self, nbr_time_point):
        self.df = pd.DataFrame(
            data=np.zeros((nbr_time_point, self.nbr_quantities)),
            columns=self.functions,
        )


class Energy(Quantity):
    def __init__(self):
        super().__init__()
        self.nbr_quantities = 3
        self.dimension = [1, 1, 1]
        self.functions = [
            "kinetic_energy",
            "potential_energy",
            "total_energy",
        ]


class Constraints(Quantity):
    def __init__(self):
        super().__init__()
        self.nbr_quantities = 2
        self.dimension = [1, 1]
        self.functions = [
            "constraint",
            "constraint_velocity",
        ]
