import numpy as np
import pandas as pd

from . import utils


class State:
    def __init__(self, manager, initial_state: list[dict,]):
        self.manager = manager
        self.initial_state = initial_state
        dim_state = utils.get_elements_dict_list(self.initial_state)

        assert (
            dim_state == self.manager.system.get_state_dimensions()
        ), "Dimension of initial states does not match dimension of system."

        nbr_states = (
            self.manager.time_stepper.nbr_time_points
        )  # this will move to manager.results

        self.columns = self.manager.system.get_state_columns()
        self.state = np.zeros(
            (nbr_states, dim_state)
        )  # this will move to manager.results
        self.state_n = np.zeros(dim_state)
        self.state_n1 = np.zeros(dim_state)

        self.time = np.zeros(nbr_states)
        initial_state_variable_names = list(self.initial_state.keys())

        if (
            not hasattr(self.manager.integrator, "variable_names")
            or initial_state_variable_names == self.manager.integrator.variable_names
        ):
            pass
        else:
            if (
                initial_state_variable_names[1] == "velocity"
                and self.manager.integrator.variable_names[1] == "momentum"
            ):
                initial_state_variable_names[1] = "momentum"

                assert (
                    initial_state_variable_names
                    == self.manager.integrator.variable_names
                ), "Transformation from velocity to momentum does not fix the problem of mismatching variable names between integrator and input."

                self.initial_state["momentum"] = (
                    self.manager.system.get_momentum_from_velocity(
                        position=self.initial_state["position"],
                        velocity=self.initial_state["velocity"],
                    )
                )
            else:
                raise utils.PydykitException(
                    "Transformation from velocity to momentum does not fix the problem of mismatching variable names between integrator and input."
                )

        # transform initial state to one array
        self.state_n = self.state_n1 = self.state[0, :] = self.build_state_vector()

    def build_state_vector(self):

        if not hasattr(self.manager.integrator, "variable_names"):
            return np.array(list(self.initial_state.values())).flatten()
        else:
            list_of_lists = [
                self.initial_state[var]
                for var in self.manager.integrator.variable_names
                if var in self.initial_state
            ]
            return np.hstack(list_of_lists)

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
