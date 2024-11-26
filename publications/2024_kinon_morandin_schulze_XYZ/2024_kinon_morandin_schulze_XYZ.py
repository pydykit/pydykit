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
fig01.show()

postprocessor.results_df["sum"] = abs(postprocessor.results_df["sum"])

fig02 = postprocessor.visualize(
    quantities=["hamiltonian_difference", "dissipated_power", "sum"],
)
fig02.show()

fig03 = postprocessor.visualize(quantities=["sum"], y_axis_scale="log")
fig03.show()

fig03 = postprocessor.visualize(quantities=["constraint"], y_axis_label="constraints")
fig03.show()

fig04 = postprocessor.visualize(
    quantities=["constraint_velocity"], y_axis_label="velocity constraints"
)
fig04.show()

# postprocessor.results_df.to_csv(f"./publications/{project}/{name}.csv", index=False)

#####

# name = "four_particle_system_MP"

# manager_2 = pydykit.managers.Manager()

# path_config_file_2 = f"./publications/{project}/{name}.yml"

# manager_2.configure_from_path(path=path_config_file_2)

# porthamiltonian_system_2 = phs.PortHamiltonianMBS(manager=manager_2)
# # creates an instance of PHS with attribute MBS
# manager_2.system = porthamiltonian_system_2

# result_2 = pydykit.results.Result(manager=manager_2)
# result_2 = manager_2.manage(result=result_2)

# df_2 = result_2.to_df()
# postprocessor_2 = postprocessors.Postprocessor(manager_2, state_results_df=df_2)
# postprocessor_2.postprocess(
#     quantities=["hamiltonian", "hamiltonian"],
#     evaluation_points=["n", "n1-n"],
# )

# postprocessor_2.postprocess(
#     quantities=["dissipated_power"],
#     evaluation_points=["n05"],
#     weighted_by_timestepsize=True,
# )
# postprocessor_2.add_sum_of(
#     quantities=["hamiltonian_difference", "dissipated_power"], name="sum"
# )

# postprocessor_2.results_df["sum"] = abs(postprocessor_2.results_df["sum"])

# fig02 = postprocessor_2.visualize(
#     quantities=["hamiltonian_difference", "dissipated_power", "sum"],
# )
# fig02.show()

# fig03 = postprocessor_2.visualize(quantities=["sum"], y_axis_scale="log")
# fig03.show()

# postprocessor_2.results_df.to_csv(f"./publications/{project}/{name}.csv", index=False)

######

# name = "four_particle_system_no_diss"

# manager_3 = pydykit.managers.Manager()

# path_config_file_3 = f"./publications/{project}/{name}.yml"

# manager_3.configure_from_path(path=path_config_file_3)

# porthamiltonian_system_3 = phs.PortHamiltonianMBS(manager=manager_3)
# # creates an instance of PHS with attribute MBS
# manager_3.system = porthamiltonian_system_3

# result_3 = pydykit.results.Result(manager=manager_3)
# result_3 = manager_3.manage(result=result_3)

# df_3 = result_3.to_df()
# postprocessor_3 = postprocessors.Postprocessor(manager_3, state_results_df=df_3)
# postprocessor_3.postprocess(
#     quantities=["hamiltonian", "hamiltonian"],
#     evaluation_points=["n", "n1-n"],
# )

# # Hamiltonian
# fig01 = postprocessor_3.visualize(quantities=["hamiltonian"])
# fig01.show()

# fig02 = postprocessor_3.visualize(
#     quantities=["hamiltonian_difference"],
# )
# fig02.show()

# postprocessor_3.results_df.to_csv(f"./publications/{project}/{name}.csv", index=False)
########


# name = "four_particle_system_blowup_DG"

# manager_4 = pydykit.managers.Manager()

# path_config_file_4 = f"./publications/{project}/{name}.yml"

# manager_4.configure_from_path(path=path_config_file_4)

# porthamiltonian_system_4 = phs.PortHamiltonianMBS(manager=manager_4)
# # creates an instance of PHS with attribute MBS
# manager_4.system = porthamiltonian_system_4

# result_4 = pydykit.results.Result(manager=manager_4)
# result_4 = manager_4.manage(result=result_4)

# df_4 = result_4.to_df()
# postprocessor_4 = postprocessors.Postprocessor(manager_4, state_results_df=df_4)
# postprocessor_4.postprocess(
#     quantities=["hamiltonian"],
#     evaluation_points=["n"],
# )

# # Hamiltonian
# fig01 = postprocessor_4.visualize(quantities=["hamiltonian"])
# fig01.show()

# postprocessor_4.results_df.to_csv(f"./publications/{project}/{name}.csv", index=False)

######

# name = "four_particle_system_blowup_MP"

# manager_5 = pydykit.managers.Manager()

# path_config_file_5 = f"./publications/{project}/{name}.yml"

# manager_5.configure_from_path(path=path_config_file_5)

# porthamiltonian_system_5 = phs.PortHamiltonianMBS(manager=manager_5)
# # creates an instance of PHS with attribute MBS
# manager_5.system = porthamiltonian_system_5

# result_5 = pydykit.results.Result(manager=manager_5)
# result_5 = manager_5.manage(result=result_5)

# df_5 = result_5.to_df()
# postprocessor_5 = postprocessors.Postprocessor(manager_5, state_results_df=df_5)
# postprocessor_5.postprocess(
#     quantities=["hamiltonian"],
#     evaluation_points=["n"],
# )

# # Hamiltonian
# fig01 = postprocessor_5.visualize(quantities=["hamiltonian"])
# fig01.show()

# postprocessor_5.results_df.to_csv(f"./publications/{project}/{name}.csv", index=False)
