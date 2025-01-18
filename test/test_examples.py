import numpy as np
import pytest

import pydykit
import pydykit.examples
from pydykit.configuration import Configuration
from pydykit.managers import Manager
from pydykit.postprocessors import Postprocessor
from pydykit.systems_port_hamiltonian import PortHamiltonianMBS

from . import utils
from .constants import A_TOL, PATH_REFERENCE_RESULTS, R_TOL

example_manager = pydykit.examples.ExampleManager()

worklist = [
    "pendulum_3d",
    "pendulum_2d",
    "two_particle_system",
    "four_particle_system_midpoint",
    "four_particle_system_discrete_gradient_dissipative",
    "visco_pendulum",
    "lorenz",
    "reactor",
    "four_particle_system_ph_discrete_gradient_dissipative",
]

phmbs = ["four_particle_system_ph_discrete_gradient_dissipative"]


class TestExamples:
    @pytest.mark.parametrize(
        ("content_config_file", "expected_result_df", "is_phmbs"),
        (
            pytest.param(
                example_manager.get_example(name=key),
                utils.load_result_of_pydykit_simulation(
                    path=PATH_REFERENCE_RESULTS.joinpath(f"{key}.csv")
                ),
                key in phmbs,
                id=key,
            )
            for key in worklist
        ),
    )
    def test_run_examples(self, content_config_file, expected_result_df, is_phmbs):

        manager = Manager()
        configuration = Configuration(
            **content_config_file,
        )
        manager.configure(configuration=configuration)

        if is_phmbs:
            # intermediate steps if conversion to PH system is necessary
            porthamiltonian_system = PortHamiltonianMBS(manager=manager)
            # creates an instance of PHS with attribute MBS
            manager.system = porthamiltonian_system

        result = manager.manage()
        old = expected_result_df
        new = result.to_df()

        if is_phmbs:
            postprocessor = Postprocessor(manager, state_results_df=new)
            postprocessor.postprocess(
                quantities_and_evaluation_points={"hamiltonian": ["current_time"]}
            )
            new = postprocessor.results_df

        utils.print_compare(old=old, new=new)

        assert np.allclose(
            old,
            new,
            rtol=R_TOL,
            atol=A_TOL,
        )
