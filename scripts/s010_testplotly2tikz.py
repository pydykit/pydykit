import plotly.express as px
import tikzplotly

# checking the ability to export plotly images to .tikz figures

df = px.data.gapminder().query("continent == 'Oceania'")
fig = px.line(df, x="year", y="lifeExp", color="country", markers=True)
fig.show()
tikzplotly.save("example.tex", fig)
