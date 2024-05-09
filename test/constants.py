from pathlib import Path

if __name__ != "__main__":
    PATH_TEST_DIRECTORY = Path(__file__).parent.absolute()
    PATH_REFERENCE_RESULTS = PATH_TEST_DIRECTORY.joinpath("reference_results")

A_TOL = 1e-5
R_TOL = 1e-5
