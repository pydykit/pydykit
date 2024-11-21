import pathlib

import plotly.express as px
import tikzplotly

import pydykit

# get absolute config file path
current_parent_path = pathlib.Path(__file__).parent.resolve()
relative_config_file_path = "../pydykit/example_files/pendulum_3d_cartesian.yml"
absolute_config_file_path = (current_parent_path / relative_config_file_path).resolve()

manager = pydykit.managers.Manager().configure_from_path(path=absolute_config_file_path)
result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)

print("Success, start plotting")

df = result.to_df()

color_palette = [
    "#0072B2",
    "#009E73",
    "#D55E00",
    "#56B4E9",
    "#CC79A7",
    "#E69F00",
    "#F0E442",
]

# Export using tikzplotlib, see https://pypi.org/project/tikzplotly/
fig = px.line(
    df,
    x="x",
    y="y",
    markers=False,
    labels={"x": "$x$", "y": "$y$"},
    color_discrete_sequence=color_palette,
)
tikzplotly.save("docs/tex_export/example_figure.tex", fig)
