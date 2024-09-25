import pathlib

import pydykit
from pydykit import postprocessors

# get absolute config file path
current_parent_path = pathlib.Path(__file__).parent.resolve()
relative_config_file_path = "../pydykit/example_files/pendulum_3d_cartesian.yml"
absolute_config_file_path = (current_parent_path / relative_config_file_path).resolve()

manager = pydykit.Manager(path_config_file=absolute_config_file_path)
result = manager.manage()

print("Success, start plotting")

df = result.to_df()

relative_postprocess_config_file_path = (
    "../pydykit/example_postprocessing_input/pendulum_3d_cartesian.yml"
)
absolute_postprocess_config_file_path = (
    current_parent_path / relative_postprocess_config_file_path
).resolve()

postprocessor = postprocessors.Postprocessor(
    manager, path_config_file=absolute_postprocess_config_file_path
)
# postprocessor.postprocess()
