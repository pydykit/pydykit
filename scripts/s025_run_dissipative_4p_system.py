import plotly.graph_objects as go

import pydykit
import pydykit.postprocessors as postprocessors

manager = pydykit.managers.Manager()
name = "four_particle_system_dissipative"
path_config_file = f"./pydykit/example_files/{name}.yml"
manager.configure_from_path(path=path_config_file)
result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)

df = result.to_df()

# postprocessor = postprocessors.Postprocessor(
#     manager,
#     results_df=df,
# )
# postprocessor.postprocess(quantities=["total_energy"])

# # Plot
# fig01 = postprocessor.visualize()
# fig01.show()

# df.to_csv(f"test/reference_results/{name}.csv")
