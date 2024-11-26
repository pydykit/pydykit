from pathlib import Path

import pytest

from .constants import PATH_PUBLICATIONS_DIRECTORY

projects = ["2024_kinon_morandin_schulze_XYZ"]


def get_python_files(directory):
    # Use Path.glob to find all .py files in the directory
    python_files = [str(file.absolute().stem) for file in Path(directory).glob("*.py")]
    return python_files


def run_script_code(script_name):
    with open(script_name) as file:
        script_content = file.read()
    exec(script_content)


class TestExamples:
    @pytest.mark.weekly
    @pytest.mark.parametrize(
        ("publication_scripts", "project"),
        (
            pytest.param(
                get_python_files(
                    directory=PATH_PUBLICATIONS_DIRECTORY.joinpath(f"{key}")
                ),
                key,
                id=key,
            )
            for key in projects
        ),
    )
    def test_run_publication_scripts(self, publication_scripts, project):

        for script in publication_scripts:
            run_script_code(
                PATH_PUBLICATIONS_DIRECTORY.joinpath(f"{project}/{script}.py")
            )
