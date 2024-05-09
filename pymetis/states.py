import numpy as np
import pandas as pd


class State:
    def __init__(self, nbr_states, dim_state, columns):
        self.columns = columns
        self.state = np.zeros((nbr_states, dim_state))
        self.state_n = np.zeros(dim_state)
        self.state_n1 = np.zeros(dim_state)

        self.time = np.zeros(nbr_states)

    def to_df(self):
        df = pd.DataFrame(
            data=self.state,
            columns=self.columns,
        )
        df["time"] = self.time
        return df
