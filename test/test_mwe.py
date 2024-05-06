from pathlib import Path

import numpy as np
import pymetis
import pymetis.examples

PATH_THIS_FILE_DIR = Path(__file__).parent.absolute()
A_TOL = 1e-5
R_TOL = 1e-5


def load_result_of_metis_simulation(path):
    import scipy.io

    mat = scipy.io.loadmat(path)
    return mat


class TestMWE:
    def test_run(self):
        config = pymetis.examples.get(name="single_analysis_pendulum")
        manager = pymetis.Manager(config=config)
        manager.solver.solve()
        result = manager.solver.result

        reference_x = load_result_of_metis_simulation(
            path=PATH_THIS_FILE_DIR.joinpath(
                "metis_references",
                "single_analysis_pendulum.m",
            )
        )

        np.allclose(
            result.x,
            reference_x,
            rtol=R_TOL,
            atol=A_TOL,
        )
