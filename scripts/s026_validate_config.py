from pathlib import Path

from pydykit.configuration import Configuration
from pydykit.utils import load_yaml_file

path = Path(__file__).parent.parent.joinpath(
    "pydykit", "example_files", "particle_system_02.yml"
)

file_content = load_yaml_file(
    path=path,
)

configuration = Configuration(
    **file_content["configuration"],
)

print(
    f"configuration.system.kwargs.particles="
    + f"\n{configuration.system.kwargs.particles}"
)
