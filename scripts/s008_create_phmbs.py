import pydykit
import pydykit.systems
import plotly.graph_objects as go


manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/porthamiltonianfourparticlesystem.yml"
)
manager.system.initialize()  # creates MBS named FourParticleSystem

PHS = pydykit.systems.PortHamiltonianMBS(manager=manager)
PHS.initialize(MultiBodySystem=manager.system)
# creates an instance of PHS with attribute MBS
manager.system = PHS

result = manager.manage()

# import scipy.io

# path = "./test/reference_results/metis/porthamiltonianfourparticlesystem.mat"
# reference = scipy.io.loadmat(path)
# old = reference["coordinates"]


# result_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# new = result.state[:, result_indices]

# """Print useful views on old and new data"""
# difference = new - old
# print(f"new.shape={new.shape}")
# print(f"old.shape={old.shape}")
# print(f"difference, i.e., new - old = {difference}")
# import numpy as np

# assert np.allclose(
#     new,
#     old,
#     rtol=1e-5,
#     atol=1e-5,
# )

df = result.to_df()

fig = go.Figure(
    data=go.Scatter3d(
        x=df["x1"],
        y=df["y1"],
        z=df["z1"],
        marker=dict(
            size=3,
            color=df["time"],
            colorscale="Viridis",
            colorbar=dict(
                thickness=20,
                title="time",
            ),
        ),
        line=dict(
            color="darkblue",
            width=3,
        ),
    )
)

fig.add_trace(
    go.Scatter3d(
        x=df["x2"],
        y=df["y2"],
        z=df["z2"],
        marker=dict(
            size=3,
            color=df["time"],
            colorscale="Viridis",
            colorbar=dict(
                thickness=20,
                title="time",
            ),
        ),
        line=dict(
            color="darkblue",
            width=3,
        ),
    )
)

fig.add_trace(
    go.Scatter3d(
        x=df["x3"],
        y=df["y3"],
        z=df["z3"],
        marker=dict(
            size=3,
            color=df["time"],
            colorscale="Viridis",
            colorbar=dict(
                thickness=20,
                title="time",
            ),
        ),
        line=dict(
            color="darkblue",
            width=3,
        ),
    )
)

fig.add_trace(
    go.Scatter3d(
        x=df["x4"],
        y=df["y4"],
        z=df["z4"],
        marker=dict(
            size=3,
            color=df["time"],
            colorscale="Viridis",
            colorbar=dict(
                thickness=20,
                title="time",
            ),
        ),
        line=dict(
            color="darkblue",
            width=3,
        ),
    )
)

fig.show()
