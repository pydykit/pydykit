import plotly.graph_objects as go

import pydykit
import pydykit.postprocessors as postprocessors
import pydykit.systems_port_hamiltonian as phs

name = "four_particle_system_ph_discrete_gradient_dissipative"

manager = pydykit.managers.Manager()

path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)

porthamiltonian_system = phs.PortHamiltonianMBS(manager=manager)
# creates an instance of PHS with attribute MBS
manager.system = porthamiltonian_system

result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)

df = result.to_df()

fig = go.Figure()

postprocessor = postprocessors.Postprocessor(manager, state_results_df=df)

for index in range(manager.system.mbs.nbr_particles):
    postprocessor.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position0_particle{index}"],
        y_components=df[f"position1_particle{index}"],
        z_components=df[f"position2_particle{index}"],
        time=df["time"],
    )
fig.show()

postprocessor.postprocess(
    quantities=[
        "hamiltonian",
        "hamiltonian",
        "constraint",
        "constraint_velocity",
    ],
    evaluation_points=[
        "current_time",
        "interval_increment",
        "current_time",
        "current_time",
    ],
)

postprocessor.postprocess(
    quantities=["dissipated_power"],
    evaluation_points=["interval_midpoint"],
    weighted_by_timestepsize=True,
)

postprocessor.add_sum_of(
    quantities=["hamiltonian_interval_increment", "dissipated_power_interval_midpoint"],
    sum_name="sum",
)

# Hamiltonian
fig01 = postprocessor.visualize(quantities=["hamiltonian_current_time"])
fig01.show()

postprocessor.results_df["sum"] = abs(postprocessor.results_df["sum"])

fig02 = postprocessor.visualize(
    quantities=[
        "hamiltonian_interval_increment",
        "dissipated_power_interval_midpoint",
        "sum",
    ],
)
fig02.show()

fig03 = postprocessor.visualize(quantities=["sum"], y_axis_scale="log")
fig03.show()

fig03 = postprocessor.visualize(
    quantities=["constraint_current_time"], y_axis_label="constraints"
)
fig03.show()

fig04 = postprocessor.visualize(
    quantities=["constraint_velocity_current_time"], y_axis_label="velocity constraints"
)
fig04.show()
