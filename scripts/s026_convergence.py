import numpy as np
import pandas as pd
import plotly.express as px

import pydykit
import pydykit.integrators
import pydykit.systems_port_hamiltonian as phs
import pydykit.time_steppers

# Define the name of the configuration file
name = "four_particle_system_convergence"
path_config_file = f"./pydykit/example_files/{name}.yml"

# Create a manager and configure it from the configuration file
manager = pydykit.managers.Manager()
manager.configure_from_path(path=path_config_file)

# store mbs system for later use
mbs_system = manager.system.copy(state=manager.system.initial_state)

porthamiltonian_system = phs.PortHamiltonianMBS(manager=manager)
# creates an instance of PHS with attribute MBS
manager.system = porthamiltonian_system

result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)


def get_final_values(result):
    df_result = result.to_df()
    final_position4_x = df_result["position0_particle3"].iloc[-1]
    final_position4_y = df_result["position1_particle3"].iloc[-1]
    final_position4_z = df_result["position2_particle3"].iloc[-1]
    final_momentum4_x = df_result["momentum0_particle3"].iloc[-1]
    final_momentum4_y = df_result["momentum1_particle3"].iloc[-1]
    final_momentum4_z = df_result["momentum2_particle3"].iloc[-1]
    final_multiplier_1 = df_result["lambda0"].iloc[-1]
    final_position = np.array([final_position4_x, final_position4_y, final_position4_z])
    final_momentum = np.array([final_momentum4_x, final_momentum4_y, final_momentum4_z])
    final_multipliers = np.array([final_multiplier_1, 0, 0])
    return final_position, final_momentum, final_multipliers


# get positions of particle 4 at the end of the simulation
reference_final_position, reference_final_momentum, reference_final_multipliers = (
    get_final_values(result=result)
)

# Create a DataFrame with one column
timestep_size = manager.time_stepper.step_size
reference_solution_column_name_position = f"final_position_reference_{timestep_size}"
reference_solution_column_name_momentum = f"final_momentum_reference_{timestep_size}"
reference_solution_column_name_multipliers = (
    f"final_multipliers_reference_{timestep_size}"
)
df = pd.DataFrame(
    {
        reference_solution_column_name_position: reference_final_position,
        reference_solution_column_name_momentum: reference_final_momentum,
        reference_solution_column_name_multipliers: reference_final_multipliers,
    }
)

# df.to_csv(
#     f"./pydykit/example_files/{name}_reference.csv",
#     index=False,
# )

# save reference timestepping attributes
reference_timestepper = manager.time_stepper
start = reference_timestepper.start
end = reference_timestepper.end

# Define the timestep sizes to compute
all_timestep_sizes = [0.01, 0.005, 0.002, 0.001]

integrator = "MidpointPH"  # "DiscreteGradientPHDAE"

for timestep_size in all_timestep_sizes:

    # Create a new instance of the same type with the new timestep size
    manager.time_stepper = type(reference_timestepper)(
        manager=manager, step_size=timestep_size, start=start, end=end
    )

    # change system to the original mbs system
    manager.system = mbs_system

    # create a new instance of the ph system and set it as the system of the manager
    new_porthamiltonian_system = phs.PortHamiltonianMBS(manager=manager)
    manager.system = new_porthamiltonian_system

    if integrator == "MidpointPH":
        manager.integrator = pydykit.integrators.MidpointPH(manager=manager)

    # create a new result object and simulate
    result = pydykit.results.Result(manager=manager)
    result = manager.manage(result=result)

    # get values at the end of the simulation
    final_position, final_momentum, final_multipliers = get_final_values(result=result)

    # Append the final position, momentum, and multipliers to the DataFrame
    df[f"final_position_{timestep_size}"] = final_position
    df[f"final_momentum_{timestep_size}"] = final_momentum
    df[f"final_multipliers_{timestep_size}"] = final_multipliers

# Save the DataFrame to a CSV file
# df.to_csv(
#     f"./pydykit/example_files/{name}_{integrator}.csv",
#     index=False,
# )

# Compute the errors
errors = {}
for timestep_size in all_timestep_sizes:
    solution_position = df[f"final_position_{timestep_size}"].to_numpy()
    error_position = np.linalg.norm(
        solution_position - reference_final_position
    ) / np.linalg.norm(reference_final_position)
    solution_momentum = df[f"final_momentum_{timestep_size}"].to_numpy()
    error_momentum = np.linalg.norm(
        solution_momentum - reference_final_momentum
    ) / np.linalg.norm(reference_final_momentum)
    solution_multipliers = df[f"final_multipliers_{timestep_size}"].to_numpy()
    error_multipliers = np.linalg.norm(
        solution_multipliers - reference_final_multipliers
    ) / np.linalg.norm(reference_final_multipliers)
    errors[timestep_size] = {
        "error_position": error_position,
        "error_momentum": error_momentum,
        "error_multipliers": error_multipliers,
    }

# Convert the dictionary to a DataFrame
errors_df = pd.DataFrame.from_dict(errors, orient="index").reset_index()
errors_df.columns = [
    "timestep_size",
    "error_position",
    "error_momentum",
    "error_multiplier",
]

# Save the errors to a CSV file
# errors_df.to_csv(
#     f"./pydykit/example_files/{name}_{integrator}_errors.csv",
#     index=False,
# )

# Create the plot using Plotly
fig = px.line(
    errors_df,
    x="timestep_size",
    y=["error_position", "error_momentum", "error_multiplier"],
    title="Convergence of the final position, momentum, and multipliers",
    labels={"Timestep size": "Timestep size", "value": "Error"},
    log_x=True,
    log_y=True,
)
fig.show()
