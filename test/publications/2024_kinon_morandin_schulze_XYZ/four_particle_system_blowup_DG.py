import pydykit
import pydykit.postprocessors as postprocessors
import pydykit.systems_port_hamiltonian as phs

project = "2024_kinon_morandin_schulze_XYZ"

name = "four_particle_system_blowup_DG"

manager_4 = pydykit.managers.Manager()

path_config_file_4 = f"./test/publications/{project}/{name}.yml"

manager_4.configure_from_path(path=path_config_file_4)

porthamiltonian_system_4 = phs.PortHamiltonianMBS(manager=manager_4)
# creates an instance of PHS with attribute MBS
manager_4.system = porthamiltonian_system_4

result_4 = pydykit.results.Result(manager=manager_4)
result_4 = manager_4.manage(result=result_4)

df_4 = result_4.to_df()
postprocessor_4 = postprocessors.Postprocessor(manager_4, state_results_df=df_4)
postprocessor_4.postprocess(
    quantities=["hamiltonian"],
    evaluation_points=["n"],
)

# Hamiltonian
fig01 = postprocessor_4.visualize(quantities=["hamiltonian"])
# fig01.show()

# postprocessor_4.results_df.to_csv(f"./publications/{project}/{name}.csv", index=False)
