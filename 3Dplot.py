import plotly.express as px
import pandas as pd

df = pd.read_excel("scores.xlsx", engine="openpyxl")

fig = px.scatter_3d(df,
    x="Privacy", y="Utility", z="Safety",
    color="Safety", text="Paper")

fig.update_coloraxes(colorbar_title="Range")

fig.show()
