import numpy as np
import pytest

import pydykit
import pydykit.examples

from . import constants, utils

example_manager = pydykit.examples.Manager()

example_worklist = [
    dict(
        name="pendulum_3d_cartesian_full_time",
        result_indices=[0, 1, 2],
    ),
    dict(
        name="rigidbodyrotatingquaternion",
        result_indices=[0, 1, 2, 3],
    ),
    dict(
        name="four_particle_system",
        result_indices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ),
    dict(
        name="four_particle_system_port_hamiltonian",
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

        manager = pydykit.Manager(content_config_file=content_config_file)

        manager.system.initialize()  # creates MBS named FourParticleSystem

        if isinstance(
            manager.integrator, pydykit.integrators.PortHamiltonianIntegrator
        ):
            # intermediate steps if conversion to PH system is necessary
            porthamiltonian_system = pydykit.systems.PortHamiltonianMBS(manager=manager)
            porthamiltonian_system.initialize(MultiBodySystem=manager.system)
            # creates an instance of PHS with attribute MBS
            manager.system = porthamiltonian_system

        result = manager.manage()

        reference = utils.load_result_of_metis_simulation(
            path=constants.PATH_REFERENCE_RESULTS.joinpath(
                "metis",
                f"{name}.mat",
            )
        )
        old = reference["coordinates"]

        new = result.state[:, result_indices]

        utils.print_compare(old=old, new=new)

        assert np.allclose(
            new,
            old,
            rtol=constants.R_TOL,
            atol=constants.A_TOL,
        )
