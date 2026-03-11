import plotly.graph_objects as go

from pydykit.configuration import Configuration
from pydykit.examples import ExampleManager
from pydykit.managers import Manager
from pydykit.plotters import Plotter

####### Simulation
file_content = ExampleManager().get_example(name="pendulum_3d")
configuration = Configuration(**file_content)  # Validate config file content

manager = Manager()
manager.configure(configuration=configuration)

result = manager.manage()  # Run the simulation

####### Plotting
df = result.to_df()
fig = go.Figure()
plotter = Plotter(results_df=df)
for index in range(manager.system.nbr_particles):
    plotter.plot_3d_trajectory(
        figure=fig,
        x_components=df[f"position0_particle{index}"],
        y_components=df[f"position1_particle{index}"],
        z_components=df[f"position2_particle{index}"],
        time=df["time"],
    )
    index_time = 0
    plotter.add_3d_annotation(
        figure=fig,
        x=df[f"position0_particle{index}"][index_time],
        y=df[f"position1_particle{index}"][index_time],
        z=df[f"position2_particle{index}"][index_time],
        text=f"start of particle {index}",
    )
plotter.fix_scene_bounds_to_extrema(figure=fig, df=df)

####### Show visualization
script_is_executed_on_local_machine = False  # You might want to change this

if script_is_executed_on_local_machine:
    fig.show()
else:
    print(
        fig.to_html(
            full_html=False,
            include_plotlyjs="cdn",
        )
    )
