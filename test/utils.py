import pandas as pd

from .constants import A_TOL, R_TOL


def load_result_of_metis_simulation(path):
    import scipy.io

    mat = scipy.io.loadmat(path)
    return mat


def load_result_of_pymetis_simulation(path):
    return pd.read_csv(
        path,
        index_col=0,
    )


def print_compare(old, new):
    """Print useful views on old and new data"""
    difference = new - old
    print(f"new.shape={new.shape}")
    print(f"old.shape={old.shape}")
    print(f"difference, i.e., new - old = {difference}")
