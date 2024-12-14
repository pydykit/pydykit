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

# Postprocessor object is initialized with manager and a state results dataframa, i.e. no previous simulation is required
postprocessor = postprocessors.Postprocessor(
    manager,
    state_results_df=df,
    postprocessed_data_from_integrator=result.postprocessed_from_integrator,
)

# the 3d plotting routine is now also a static method of this postprocessing object
for index in range(manager.system.mbs.nbr_particles):
    postprocessor.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position0_particle{index}"],
        y_components=df[f"position1_particle{index}"],
        z_components=df[f"position2_particle{index}"],
        time=df["time"],
    )
fig.show()

# Here, we compute different quantities, which are methods of the "system" in some specified ways
postprocessor.postprocess(
    quantities=[
        "hamiltonian",
        "hamiltonian",
        "constraint",
        "constraint_velocity",
    ],
    evaluation_points=[
        "current_time",  # this gives a simple computation of hamiltonian at each discrete point in time
        "interval_increment",  # this evaluation strategy computes increments between the current and next point in time
        "current_time",
        "current_time",
    ],
)

# in contrast to above, "dissipated_work" is a quantity that depends on the integrator, therefore it has been logged during the simulation
postprocessor.postprocess(
    quantities=["dissipated_work"],
    evaluation_points=[
        "interval_midpoint"
    ],  # it has been evaluated and interval midpoints
)

# functionality to compute sum of different columns
postprocessor.add_sum_of(
    quantities=["hamiltonian_interval_increment", "dissipated_work_interval_midpoint"],
    sum_name="sum",
)

# Visualization, column names are concatenated from "quantities" and "evaluation_points"
fig01 = postprocessor.visualize(quantities=["hamiltonian_current_time"])
fig01.show()

# you can work directly on the columns to manipulate them
postprocessor.results_df["sum"] = abs(postprocessor.results_df["sum"])

# you can plot multiple columns at once
fig02 = postprocessor.visualize(
    quantities=[
        "hamiltonian_interval_increment",
        "dissipated_work_interval_midpoint",
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
