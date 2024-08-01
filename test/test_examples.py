import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import pydykit
import pydykit.examples

from . import utils
from .constants import A_TOL, PATH_REFERENCE_RESULTS, R_TOL

example_manager = pydykit.examples.Manager()


class TestExamples:
    @pytest.mark.parametrize(
        ("content_config_file", "expected_result_df"),
        (
            pytest.param(
                example_manager.get_example(name=key),
                utils.load_result_of_pydykit_simulation(
                    path=PATH_REFERENCE_RESULTS.joinpath(f"{key}.csv")
                ),
                id=key,
            )
            for key in example_manager.list_examples()
            if key
            not in [
                "pendulum3dcartesian_full_time",
                "rigidbodyrotatingquaternion",
            ]
        ),
    )
    def test_run_examples(self, content_config_file, expected_result_df):
        manager = pydykit.Manager(content_config_file=content_config_file)
        result = manager.manage()
        old = expected_result_df
        new = result.to_df()

        utils.print_compare(old=old, new=new)

        assert np.allclose(
            old,
            new,
            rtol=R_TOL,
            atol=A_TOL,
        )
