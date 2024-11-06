import numpy as np
import pytest

import pydykit
import pydykit.examples

from . import utils
from .constants import A_TOL, PATH_REFERENCE_RESULTS, R_TOL

example_manager = pydykit.examples.Manager()

example_worklist = [
    "four_particle_system_ph_discrete_gradient",
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

        manager = pydykit.managers.Manager()
        configuration = pydykit.configuration.Configuration(
            **content_config_file["configuration"],
        )
        manager._configure(configuration=configuration)

        # intermediate steps if conversion to PH system is necessary
        porthamiltonian_system = pydykit.systems_port_hamiltonian.PortHamiltonianMBS(
            manager=manager
        )
        # creates an instance of PHS with attribute MBS
        manager.system = porthamiltonian_system

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
