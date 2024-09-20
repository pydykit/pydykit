import numpy as np
import abc


class Postprocessor:

    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

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

    def initialize_postprocessing_quantities(self):
        pass

    #     for quantity in self.quantity_names:
    #         quantity_instance = globals()[quantity]()
    #         setattr(self, quantity, quantity_instance)
    #         pass
    #         # self.__setattr__(name=quantity) = eval(quantity)


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
