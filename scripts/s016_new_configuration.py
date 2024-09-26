import pydykit
import pydykit.configuration
from pydykit import utils

name = "particle_system_02"
path_config_file = f"./pydykit/example_files/{name}.yml"


file_content = utils.load_yaml_file(
    path=path_config_file,
)
configuration = pydykit.configuration.Configuration(**file_content["configuration"])

manager = pydykit.managers.Manager()
manager.configure(configuration=configuration)

result = manager.manage()
df = result.to_df()
# df.to_csv("test/reference_results/pendulum_2d.csv")
