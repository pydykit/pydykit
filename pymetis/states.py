import numpy as np


class States:
    def __init__(self, nbr_states, dim_state):
        self.state = np.zeros((nbr_states, dim_state))
        self.state_n = np.zeros(dim_state)
        self.state_n1 = np.zeros(dim_state)

        self.time = np.zeros(nbr_states)
