from pathlib import Path

import numpy as np
import pymetis
import pymetis.examples
import pytest

from . import constants

if __name__ != "__main__":
    PATH_THIS_FILE_DIR = constants.PATH_TEST_DIRECTORY
else:
    PATH_THIS_FILE_DIR = Path.cwd().joinpath("test")


def load_result_of_metis_simulation(path):
    import scipy.io

    mat = scipy.io.loadmat(path)
    return mat


example_manager = pymetis.examples.Manager()


class TestCompareWithMetis:
    @pytest.mark.parametrize(
        ("content_config_file", "name"),
        (
            pytest.param(
                example_manager.get_example(name=key),
                key,
                id=key,
            )
            for key in ["pendulum3dcartesian_full_time"]
        ),
    )
    def test_run(self, content_config_file, name):

        manager = pymetis.Manager(content_config_file=content_config_file)
        result = manager.manage()

        reference = load_result_of_metis_simulation(
            path=PATH_THIS_FILE_DIR.joinpath(
                "metis_reference_results",
                f"{name}.mat",
            )
        )
        reference_coordinates = reference["coordinates"]

        np.allclose(
            result.state[:, [0, 1, 2]],
            reference_coordinates,
            rtol=constants.R_TOL,
            atol=constants.A_TOL,
        )
