import pydykit
import pydykit.postprocessors as postprocessors
import pydykit.systems_port_hamiltonian as phs

project = "2024_kinon_morandin_schulze_XYZ"

name = "four_particle_system_blowup_MP"

manager_5 = pydykit.managers.Manager()

path_config_file_5 = f"./test/publications/{project}/{name}.yml"

manager_5.configure_from_path(path=path_config_file_5)

porthamiltonian_system_5 = phs.PortHamiltonianMBS(manager=manager_5)
# creates an instance of PHS with attribute MBS
manager_5.system = porthamiltonian_system_5

result_5 = pydykit.results.Result(manager=manager_5)
result_5 = manager_5.manage(result=result_5)

df_5 = result_5.to_df()
postprocessor_5 = postprocessors.Postprocessor(manager_5, state_results_df=df_5)
postprocessor_5.postprocess(
    quantities=["hamiltonian"],
    evaluation_points=["n"],
)

# Hamiltonian
fig01 = postprocessor_5.visualize(quantities=["hamiltonian"])
# fig01.show()

# postprocessor_5.results_df.to_csv(f"./publications/{project}/{name}.csv", index=False)
