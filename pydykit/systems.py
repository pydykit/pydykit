import copy

import numpy as np

from . import utils


class System:
    # inspired by mixin classes approach
    def copy(self, state):
        new = copy.deepcopy(self)
        new.state = state
        return new

    def initialize_state(self, state):

        # convert state as dict to array with values
        self.initial_state = state
        self.dim_state = utils.get_nbr_elements_dict_list(self.initial_state)
        self.state_columns = self.get_state_columns()
        self.build_state_vector()

    def build_state_vector(self):
        self.state = np.hstack(list(self.initial_state.values()))
