import pydykit
import pydykit.configuration
from pydykit import utils
from pydykit.results import Result

manager = pydykit.managers.Manager()


name = "two_particle_system"
path_config_file = f"./pydykit/example_files/{name}.yml"

# file_content = utils.load_yaml_file(
#     path=path_config_file,
# )
# configuration = pydykit.configuration.Configuration(**file_content)
# manager.configure(configuration=configuration)

manager.configure_from_path(path=path_config_file)

result = Result(manager=manager)
result = manager.manage(result=result)
df = result.to_df()
# df.to_csv("test/reference_results/pendulum_2d.csv")
