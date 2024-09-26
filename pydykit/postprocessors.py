import abc
import copy
import importlib
import inspect

import numpy as np
import pandas as pd

from . import utils


class Postprocessor:

    def __init__(self, manager, path_config_file=None, content_config_file=None):

        if (path_config_file is not None) and (content_config_file is not None):
            raise utils.pydykitException(
                "Did receive both path_config_file and content_config_file. "
                + "Supply either path_config_file or content_config_file, not both"
            )
        elif path_config_file is not None:
            self.path_config_file = path_config_file
            self.content_config_file = utils.load_yaml_file(path=self.path_config_file)
        elif content_config_file is not None:
            self.content_config_file = content_config_file
        else:
            raise utils.pydykitException(
                "Did not receive kwargs. "
                + "Supply either path_config_file or content_config_file"
            )

        self.name = self.content_config_file["name"]
        self.configuration = self.content_config_file["configuration"]

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

    def postprocess(self, dataframe):
        system = self.manager.system
        self.nbr_time_point = len(dataframe)

        for quantity in self.configuration["quantity_names"]:
            quantity_instance = getattr(self, quantity)
            quantity_instance.create_dataframe(nbr_time_point=self.nbr_time_point)

        del dataframe["time"]
        for step_index in range(self.nbr_time_point):
            row = dataframe.iloc[step_index]
            state = row.to_numpy()
            q, p, lambd = system.decompose_state(state)

            for quantity in self.configuration["quantity_names"]:
                function_list = globals()[quantity]().functions
                quantity_instance = getattr(self, quantity)
                for function in function_list:
                    system_function = getattr(system, function)
                    args_list = inspect.getfullargspec(system_function)[0]
                    args_list.remove("self")
                    print(args_list)
                    if args_list == ["q", "p"]:
                        z = [q, p]
                    elif args_list == ["q"]:
                        z = [q]
                    elif args_list == ["p"]:
                        z = [p]
                    else:
                        raise Exception("Not implemented")

                    input_dict = dict(zip(args_list, z))
                    quantity_instance.df.at[step_index, function] = system_function(
                        **input_dict
                    )

        # # create new_df
        #     self.df = merge all dataframes
        #
        # merge with input dataframe

        # return merged dataframe
        for quantity in self.configuration["quantity_names"]:
            quantity_instance = getattr(self, quantity)
            dataframe = pd.concat([dataframe, quantity_instance.df], axis=1)

        return dataframe


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
