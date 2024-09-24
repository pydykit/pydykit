import pydykit
import pathlib

# get absolute config file path
current_parent_path = pathlib.Path(__file__).parent.resolve()
relative_config_file_path = "../pydykit/example_files/pendulum3dcartesian.yml"
absolute_config_file_path = (current_parent_path / relative_config_file_path).resolve()

manager = pydykit.Manager(path_config_file=absolute_config_file_path)
result = manager.manage()

print("Success, start plotting")

df = result.to_df()

manager.postprocess()
