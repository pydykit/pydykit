import pydykit
import pydykit.postprocessors as postprocessors
import pydykit.systems_port_hamiltonian as phs

project = "2024_kinon_morandin_schulze_XYZ"
name = "four_particle_system"

manager = pydykit.managers.Manager()

path_config_file = f"./publications/{project}/{name}.yml"

manager.configure_from_path(path=path_config_file)

porthamiltonian_system = phs.PortHamiltonianMBS(manager=manager)
# creates an instance of PHS with attribute MBS
manager.system = porthamiltonian_system

result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)

df = result.to_df()
postprocessor = postprocessors.Postprocessor(manager, state_results_df=df)
postprocessor.postprocess(
    quantities=["hamiltonian", "hamiltonian", "constraint", "constraint_velocity"],
    evaluation_points=["n", "n1-n", "n", "n"],
)

postprocessor.postprocess(
    quantities=["dissipated_power"],
    evaluation_points=["n05"],
    weighted_by_timestepsize=True,
)
postprocessor.add_sum_of(
    quantities=["hamiltonian_difference", "dissipated_power"], name="sum"
)

# Hamiltonian
fig01 = postprocessor.visualize(quantities=["hamiltonian"])
# fig01.show()

postprocessor.results_df["sum"] = abs(postprocessor.results_df["sum"])

fig02 = postprocessor.visualize(
    quantities=["hamiltonian_difference", "dissipated_power", "sum"],
)
# fig02.show()

fig03 = postprocessor.visualize(quantities=["sum"], y_axis_scale="log")
# fig03.show()

fig03 = postprocessor.visualize(quantities=["constraint"], y_axis_label="constraints")
# fig03.show()

fig04 = postprocessor.visualize(
    quantities=["constraint_velocity"], y_axis_label="velocity constraints"
)
# fig04.show()

# postprocessor.results_df.to_csv(f"./publications/{project}/{project}.csv", index=False)
