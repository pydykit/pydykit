from pathlib import Path

import numpy as np
import pymetis
import pymetis.examples
import pytest

from .constants import A_TOL, R_TOL

example_manager = pymetis.examples.Manager()


class TestExamples:
    @pytest.mark.parametrize(
        ("content_config_file", "expected_result"),
        (
            pytest.param(
                example_manager.get_example(name=key),
                None,
                id=key,
            )
            for key in example_manager.list_examples()
        ),
    )
    def test_run(self, content_config_file, expected_result):
        manager = pymetis.Manager(content_config_file=content_config_file)
        manager.manage()
