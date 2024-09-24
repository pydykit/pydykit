import numpy as np
import pandas as pd


def load_result_of_metis_simulation(path):
    import scipy.io

    mat = scipy.io.loadmat(path)
    return mat


ref = load_result_of_metis_simulation(
    path="test/reference_results/metis/pendulum_3d_cartesian_full_time.mat"
)

df = pd.DataFrame(
    data=np.concatenate(
        [ref["coordinates"], ref["momenta"], ref["multiplier"], ref["time"].T], axis=1
    ),
    columns=["x", "y", "z", "p_x", "p_y", "p_z", "lambda", "time"],
)


df.to_csv("test/reference_results/metis/pendulum_3d_cartesian_full_time.csv")
