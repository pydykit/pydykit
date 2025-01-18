from pathlib import Path

import numpy as np
import pytest

import pydykit
import pydykit.examples
from pydykit.configuration import Configuration
from pydykit.managers import Manager
from pydykit.results import Result
from pydykit.utils import load_yaml_file

from . import constants, utils

path_config_files_directory = Path(__file__).parent.joinpath("config_files")

worklist = [
    dict(
        name="pendulum_3d",
        result_indices=[0, 1, 2],
    ),
    dict(
        name="rigid_body_rotating_quaternion",
        result_indices=[0, 1, 2, 3],
    ),
    dict(
        name="four_particle_system_midpoint",
        result_indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ),
    dict(
        name="four_particle_system_discrete_gradient_dissipative",
        result_indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ),
]


class TestCompareWithMetis:
    @pytest.mark.parametrize(
        ("content_config_file", "name", "result_indices"),
        (
            pytest.param(
                load_yaml_file(
                    path=path_config_files_directory.joinpath(task["name"] + ".yml")
                ),
                task["name"],
                task["result_indices"],
                id=task["name"],
            )
            for task in worklist
        ),
    )
    @pytest.mark.slow
    def test_run(self, content_config_file, name, result_indices):

        manager = Manager()
        configuration = Configuration(
            **content_config_file,
        )
        manager._configure(configuration=configuration)
        result = Result(manager=manager)
        result = manager.manage(result=result)

        reference = utils.load_result_of_metis_simulation(
            path=constants.PATH_REFERENCE_RESULTS.joinpath(
                "metis",
                f"{name}.mat",
            )
        )
        old = reference["coordinates"]

        new = result.results[:, result_indices]

        utils.print_compare(old=old, new=new)

        assert np.allclose(
            new,
            old,
            rtol=constants.R_TOL,
            atol=constants.A_TOL,
        )
