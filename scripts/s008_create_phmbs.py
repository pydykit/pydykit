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

for index in range(manager.system.mbs.nbr_particles):
    pydykit.plotting.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position0_particle{index}"],
        y_components=df[f"position1_particle{index}"],
        z_components=df[f"position2_particle{index}"],
        time=df["time"],
    )


fig.show()

postprocessor = postprocessors.Postprocessor(manager, state_results_df=df)
postprocessor.postprocess(
    quantities=["hamiltonian", "constraint", "constraint_velocity"]
)

# Hamiltonian
fig01 = postprocessor.visualize(quantities="hamiltonian")
fig01.show()

fig02 = postprocessor.visualize(quantities="constraint", y_axis_label="constraints")
fig02.show()

fig03 = postprocessor.visualize(
    quantities="constraint_velocity", y_axis_label="velocity constraints"
)
fig03.show()
