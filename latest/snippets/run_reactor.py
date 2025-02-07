import plotly.graph_objects as go

from pydykit.configuration import Configuration
from pydykit.examples import ExampleManager
from pydykit.managers import Manager
from pydykit.plotters import Plotter

####### Simulation
file_content = ExampleManager().get_example(name="reactor")
configuration = Configuration(**file_content)  # Validate config file content

manager = Manager()
manager.configure(configuration=configuration)

result = manager.manage()  # Run the simulation

####### Plotting
fig = go.Figure()
df = result.to_df()
plotter = Plotter(results_df=df)
plotter.plot_3d_trajectory(
    figure=fig,
    x_components=df["concentration"],
    y_components=df["temperature"],
    z_components=df["reaction_rate"],
    time=df["time"],
)

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
