import pandas as pd
import plotly.graph_objects as go

import pydykit
import pydykit.postprocessors as postprocessors
import pydykit.systems_port_hamiltonian as phs

name = "four_particle_system_ph_discrete_gradient"

manager = pydykit.managers.Manager()

path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)

porthamiltonian_system = phs.PortHamiltonianMBS(manager=manager)
# creates an instance of PHS with attribute MBS
manager.system = porthamiltonian_system

result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)

df = result.to_df()
postprocessor = postprocessors.Postprocessor(manager, state_results_df=df)

fig = go.Figure()

for index in range(manager.system.mbs.nbr_particles):
    postprocessor.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position0_particle{index}"],
        y_components=df[f"position1_particle{index}"],
        z_components=df[f"position2_particle{index}"],
        time=df["time"],
    )


fig.show()

df.to_csv(f"test/reference_results/{name}.csv", index=False)

df = pd.read_csv(f"test/reference_results/{name}.csv")


postprocessor = postprocessors.Postprocessor(
    manager,
    state_results_df=df,
)
postprocessor.postprocess(
    quantities=["hamiltonian"], evaluation_points=["current_time"]
)


# Plot parts of the state together with newly calculated quantity
fig02 = postprocessor.visualize(
    quantities=["hamiltonian_current_time"]
    + [f"position{index}_particle0" for index in [0, 1, 2]],
    y_axis_label="position",
)
fig02.show()

# Plot additional data into existing graph
fig03 = postprocessor.visualize(
    quantities=[f"position{index}_particle1" for index in [0, 1, 2]],
    y_axis_label="position",
    figure=fig02,
)
fig03.show()
