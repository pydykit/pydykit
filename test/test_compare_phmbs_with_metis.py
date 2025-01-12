import numpy as np
import pytest

import pydykit
import pydykit.examples
import pydykit.systems_port_hamiltonian as phs
from pydykit.configuration import Configuration
from pydykit.managers import Manager
from pydykit.results import Result

from . import constants, utils

example_manager = pydykit.examples.ExampleManager()

example_worklist = [
    dict(
        name="four_particle_system_ph_midpoint",
        result_indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ),
    dict(
        name="four_particle_system_ph_discrete_gradient_dissipative",
        result_indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ),
]


class TestCompareWithMetis:
    @pytest.mark.parametrize(
        ("content_config_file", "name", "result_indices"),
        (
            pytest.param(
                example_manager.get_example(name=example["name"]),
                example["name"],
                example["result_indices"],
                id=example["name"],
            )
            for example in example_worklist
        ),
    )
    @pytest.mark.slow
    def test_run(self, content_config_file, name, result_indices):

        manager = Manager()
        configuration = Configuration(
            **content_config_file,
        )
        manager._configure(configuration=configuration)

        # intermediate steps if conversion to PH system is necessary
        porthamiltonian_system = phs.PortHamiltonianMBS(manager=manager)
        # creates an instance of PHS with attribute MBS
        manager.system = porthamiltonian_system

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
