import numpy as np
import pandas as pd


class State:
    def __init__(self, manager):

        nbr_states = manager.time_stepper.nbr_time_points
        dim_state = manager.system.get_state_dimensions()

        self.columns = manager.system.get_state_columns()
        self.state = np.zeros((nbr_states, dim_state))
        self.state_n = np.zeros(dim_state)
        self.state_n1 = np.zeros(dim_state)

        self.time = np.zeros(nbr_states)

        self.state_n = self.state_n1 = self.state[0, :] = (
            manager.system.initialize_states()
        )

    def to_df(self):
        df = pd.DataFrame(
            data=self.state,
            columns=self.columns,
        )
        df["time"] = self.time
        return df

    @staticmethod
    def from_df(df, step_index):
        row = df.iloc[step_index]
        row = row.drop("time")
        return row.to_numpy()
