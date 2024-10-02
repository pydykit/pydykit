import plotly.graph_objects as go

import pydykit

name = "four_particle_system_port_hamiltonian"

manager = pydykit.managers.Manager()

path_config_file = f"./pydykit/example_files/{name}.yml"

manager.configure_from_path(path=path_config_file)

porthamiltonian_system = pydykit.systems.PortHamiltonianMBS(manager=manager)
# creates an instance of PHS with attribute MBS
manager.system = porthamiltonian_system

result = manager.manage()

df = result.to_df()

fig = go.Figure()

pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position1"],
    y_components=df["position2"],
    z_components=df["position3"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position4"],
    y_components=df["position5"],
    z_components=df["position6"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position7"],
    y_components=df["position8"],
    z_components=df["position9"],
    time=df["time"],
)
pydykit.plotting.plot_3d_trajectory(
    figure=fig,
    x_components=df["position10"],
    y_components=df["position11"],
    z_components=df["position12"],
    time=df["time"],
)

fig.show()
