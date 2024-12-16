import numpy as np
import pytest

import pydykit
import pydykit.examples
import pydykit.postprocessors as postprocessors
import pydykit.systems_port_hamiltonian as phs

from . import utils
from .constants import A_TOL, PATH_REFERENCE_RESULTS, R_TOL

example_manager = pydykit.examples.Manager()

example_worklist = [
    "four_particle_system_ph_discrete_gradient",
    "four_particle_system_ph_discrete_gradient_dissipative",
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
        porthamiltonian_system = phs.PortHamiltonianMBS(manager=manager)
        # creates an instance of PHS with attribute MBS
        manager.system = porthamiltonian_system

        result = pydykit.results.Result(manager=manager)
        result = manager.manage(result=result)
        new = result.to_df()

        postprocessor = postprocessors.Postprocessor(manager, state_results_df=new)
        postprocessor.postprocess(
            quantities_and_evaluation_points={"hamiltonian": ["current_time"]}
        )

        old = expected_result_df
        new = postprocessor.results_df

        utils.print_compare(old=old, new=new)

        assert np.allclose(
            old,
            new,
            rtol=R_TOL,
            atol=A_TOL,
        )
