import plotly.graph_objects as go

import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/particle_system.yml"
)

result = manager.manage()

q, p, lambd = manager.system.decompose_state(manager.system.states.state_n)
tmp = manager.system.internal_potential(q=q)
print(tmp)

df = result.to_df()
fig = go.Figure()

for index in range(manager.system.nbr_particles):
    index = pydykit.utils.shift_index_python_to_literature(index)

    pydykit.utils.plot_three_dimensional_trajectory(
        figure=fig,
        x_components=df[f"x{index}"],
        y_components=df[f"y{index}"],
        z_components=df[f"z{index}"],
        time=df["time"],
    )


fig.update_layout(font_family="Serif")

fig.show()
