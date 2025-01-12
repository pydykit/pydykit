import numpy as np
import pytest

import pydykit
import pydykit.examples
from pydykit.configuration import Configuration
from pydykit.managers import Manager
from pydykit.results import Result

from . import utils
from .constants import A_TOL, PATH_REFERENCE_RESULTS, R_TOL

example_manager = pydykit.examples.ExampleManager()

example_worklist = [
    "pendulum_3d",
    "pendulum_2d",
    "two_particle_system",
    "four_particle_system_midpoint",
    "four_particle_system_discrete_gradient_dissipative",
    "visco_pendulum",
    "lorenz",
    "reactor",
]


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
            for key in example_worklist
        ),
    )
    def test_run_examples(self, content_config_file, expected_result_df):

        manager = Manager()
        configuration = Configuration(
            **content_config_file,
        )
        manager._configure(configuration=configuration)

        result = Result(manager=manager)
        result = manager.manage(result=result)
        old = expected_result_df
        new = result.to_df()

        utils.print_compare(old=old, new=new)

        assert np.allclose(
            old,
            new,
            rtol=R_TOL,
            atol=A_TOL,
        )
