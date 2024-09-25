import abc
import copy
import importlib

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
            pass

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

    def postprocess(self):
        system = self.manager.system
        self.nbr_time_point = self.manager.time_stepper.nbr_time_points
        self.initialize_postprocessing_quantities()

        # for i in range(NT):
        #     # extract states of current time

        #     match self.quantities:
        #         case "Energy":
        #             kinetic_energy[i] = system.get_kinetic_energy(q=position)

        # # create new_df
        # return new_df


class Quantity(abc.ABC):

    def __init__(self):
        pass


class Energy(Quantity):
    def __init__(self):
        super().__init__()
        self.nbr_quantities = 3
        self.dimension = [1, 1, 1]
        self.names = [
            "kinetic_energy",
            "potential_energy",
            "total_energy",
        ]
        self.functions = [
            "get_kinetic_energy",
            "get_potential_energy",
            "get_total_energy",
        ]


class Constraints(Quantity):
    def __init__(self):
        super().__init__()
        self.nbr_quantities = 2
        self.dimension = [1, 1]
        self.names = ["constraint_position", "constraint_velocity"]
        self.functions = [
            "constraint",
            "constraint_velocity",
        ]
