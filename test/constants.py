from pathlib import Path

if __name__ != "__main__":
    PATH_TEST_DIRECTORY = Path(__file__).parent.absolute()
    PATH_REFERENCE_RESULTS = PATH_TEST_DIRECTORY.joinpath("reference_results")
    PATH_CONFIG_FILES = PATH_TEST_DIRECTORY.joinpath("config_files")

    # ATTENTION: Iif you set OVERWRITE_EXISTING_RESULTS to True,
    # the tests will overwrite the reference results. So handle with care!
    OVERWRITE_EXISTING_RESULTS = False

A_TOL = 1e-5
R_TOL = 1e-5
