import numpy as np


class Postprocessor:

    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.__dict__.update(kwargs)

    def postprocess(self):
        system = self.manager.system
        # extract states
        # extract number of time stamps NT
        # preallocate space for postprocessed quantities

        for i in range(NT):
            # extract states of current time

            match self.quantities:
                case "Energy":
                    kinetic_energy[i] = system.get_kinetic_energy(q=position)

        # create new_df
        return new_df
