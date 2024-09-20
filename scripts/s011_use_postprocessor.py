import pydykit
import pathlib
import plotly.express as px
import tikzplotly

# get absolute config file path
current_parent_path = pathlib.Path(__file__).parent.resolve()
relative_config_file_path = "../pydykit/example_files/pendulum3dcartesian.yml"
absolute_config_file_path = (current_parent_path / relative_config_file_path).resolve()

manager = pydykit.Manager(path_config_file=absolute_config_file_path)
result = manager.manage()

print("Success, start plotting")

df = result.to_df()

manager.postprocess(df)

# color scheme (color-blind friendly)
# https://clauswilke.com/dataviz/color-pitfalls.html#not-designing-for-color-vision-deficiency
my_color_palette = [
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
    markers=True,
    labels={"x": "$x$", "y": "$y$"},
    color_discrete_sequence=my_color_palette,
)

fig.show()

tikzplotly.save("docs/tex_export/example_figure.tex", fig)
