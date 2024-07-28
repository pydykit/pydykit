import numpy as np
import pydykit
import pydykit.examples
import pytest

from . import constants, utils

example_manager = pydykit.examples.Manager()


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
    @pytest.mark.slow
    def test_run(self, content_config_file, name):

        manager = pydykit.Manager(content_config_file=content_config_file)
        result = manager.manage()

        reference = utils.load_result_of_metis_simulation(
            path=constants.PATH_REFERENCE_RESULTS.joinpath(
                "metis",
                f"{name}.mat",
            )
        )
        old = reference["coordinates"]
        new = result.state[:, [0, 1, 2]]

        utils.print_compare(old=old, new=new)

        assert np.allclose(
            new,
            old,
            rtol=constants.R_TOL,
            atol=constants.A_TOL,
        )
