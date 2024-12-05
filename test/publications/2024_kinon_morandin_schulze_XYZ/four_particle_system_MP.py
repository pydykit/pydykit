import pydykit
import pydykit.postprocessors as postprocessors
import pydykit.systems_port_hamiltonian as phs

project = "2024_kinon_morandin_schulze_XYZ"

name = "four_particle_system_MP"

manager_2 = pydykit.managers.Manager()

path_config_file_2 = f"./test/publications/{project}/{name}.yml"

manager_2.configure_from_path(path=path_config_file_2)

porthamiltonian_system_2 = phs.PortHamiltonianMBS(manager=manager_2)
# creates an instance of PHS with attribute MBS
manager_2.system = porthamiltonian_system_2

result_2 = pydykit.results.Result(manager=manager_2)
result_2 = manager_2.manage(result=result_2)

df_2 = result_2.to_df()
postprocessor_2 = postprocessors.Postprocessor(manager_2, state_results_df=df_2)
postprocessor_2.postprocess(
    quantities=["hamiltonian", "hamiltonian"],
    evaluation_points=["n", "n1-n"],
)

postprocessor_2.postprocess(
    quantities=["dissipated_power"],
    evaluation_points=["n05"],
    weighted_by_timestepsize=True,
)
postprocessor_2.add_sum_of(
    quantities=["hamiltonian_difference", "dissipated_power"], name="sum"
)

postprocessor_2.results_df["sum"] = abs(postprocessor_2.results_df["sum"])

fig02 = postprocessor_2.visualize(
    quantities=["hamiltonian_difference", "dissipated_power", "sum"],
)
# fig02.show()

fig03 = postprocessor_2.visualize(quantities=["sum"], y_axis_scale="log")
# fig03.show()

# postprocessor_2.results_df.to_csv(
#     f"./test/publications/{project}/{name}.csv", index=False
# )
