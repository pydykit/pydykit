from pathlib import Path

import numpy as np
import pymetis
import pymetis.examples
import pytest

from . import constants, utils

PATH_THIS_FILE_DIR = constants.PATH_TEST_DIRECTORY


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

        reference = utils.load_result_of_metis_simulation(
            path=PATH_THIS_FILE_DIR.joinpath(
                "metis_reference_results",
                f"{name}.mat",
            )
        )
        reference = reference["coordinates"]
        new = result.state[:, [0, 1, 2]]
        difference = new - reference

        print(f"new.shape={new.shape}")
        print(f"reference.shape={reference.shape}")
        print(f"difference = {difference}")

        assert np.allclose(
            new,
            reference,
            rtol=constants.R_TOL,
            atol=constants.A_TOL,
        )
