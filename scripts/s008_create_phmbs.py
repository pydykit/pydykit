import pydykit
import pydykit.systems
import plotly.graph_objects as go
import pydykit.utils


manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/porthamiltonianfourparticlesystem.yml"
)
manager.system.initialize()  # creates MBS named FourParticleSystem

porthamiltonian_system = pydykit.systems.PortHamiltonianMBS(manager=manager)
porthamiltonian_system.initialize(MultiBodySystem=manager.system)
# creates an instance of PHS with attribute MBS
manager.system = porthamiltonian_system

result = manager.manage()

df = result.to_df()

fig = go.Figure()

pydykit.utils.plot_three_dimensional_trajectory(
    existing_figure=fig,
    x_components=df["x1"],
    y_components=df["y1"],
    z_components=df["z1"],
    time=df["time"],
)
pydykit.utils.plot_three_dimensional_trajectory(
    existing_figure=fig,
    x_components=df["x2"],
    y_components=df["y2"],
    z_components=df["z2"],
    time=df["time"],
)
pydykit.utils.plot_three_dimensional_trajectory(
    existing_figure=fig,
    x_components=df["x3"],
    y_components=df["y3"],
    z_components=df["z3"],
    time=df["time"],
)
pydykit.utils.plot_three_dimensional_trajectory(
    existing_figure=fig,
    x_components=df["x4"],
    y_components=df["y4"],
    z_components=df["z4"],
    time=df["time"],
)

fig.show()
