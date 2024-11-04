import numpy as np
import pandas as pd
from dependency_injector.wiring import Provide, inject

from . import containers


class Result:
    @inject
    def __init__(self, manager=Provide[containers.Container.manager]):
        self.manager = manager
        self.results = np.zeros(
            (self.manager.time_stepper.nbr_time_points, self.manager.system.dim_state)
        )
        self.times = np.zeros((self.manager.time_stepper.nbr_time_points))

        self.results[0, :] = self.manager.system.state

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(
            data=self.results,
            columns=self.manager.system.state_columns,
        )
        df["time"] = self.times
        return df
