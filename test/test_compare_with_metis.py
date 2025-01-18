import numpy as np
import pytest

from pydykit.configuration import Configuration
from pydykit.managers import Manager
from pydykit.results import Result
from pydykit.utils import load_yaml_file

from .constants import A_TOL, PATH_CONFIG_FILES, PATH_REFERENCE_RESULTS, R_TOL
from .utils import load_result_of_metis_simulation, print_compare

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
                load_yaml_file(path=PATH_CONFIG_FILES.joinpath(task["name"] + ".yml")),
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

        reference = load_result_of_metis_simulation(
            path=PATH_REFERENCE_RESULTS.joinpath(
                "metis",
                f"{name}.mat",
            )
        )
        old = reference["coordinates"]

        new = result.results[:, result_indices]

        print_compare(old=old, new=new)

        assert np.allclose(
            new,
            old,
            rtol=R_TOL,
            atol=A_TOL,
        )
