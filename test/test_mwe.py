from pathlib import Path

import numpy as np
import pymetis
import pymetis.examples

from . import constants

if __name__ != "__main__":
    PATH_THIS_FILE_DIR = constants.PATH_TEST_DIRECTORY
else:
    PATH_THIS_FILE_DIR = Path.cwd().joinpath("test")


def load_result_of_metis_simulation(path):
    import scipy.io

    mat = scipy.io.loadmat(path)
    return mat


class TestMWE:
    def test_run(self):
        config = pymetis.examples.Manager().get_example(name="single_analysis_pendulum")
        manager = pymetis.Manager(content_config_file=config)
        # manager.solver.solve()
        # result = manager.solver.result

        reference = load_result_of_metis_simulation(
            path=PATH_THIS_FILE_DIR.joinpath(
                "metis_reference_results",
                "single_analysis_pendulum.mat",
            )
        )
        reference_coordinates = reference["coordinates"]

        np.allclose(
            result.coordinates,
            reference_coordinates,
            rtol=constants.R_TOL,
            atol=constants.A_TOL,
        )
