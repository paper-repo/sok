import plotly.express as px
import pandas as pd

df = pd.read_excel("scores.xlsx", engine="openpyxl")

fig = px.scatter_3d(
    df,
    x="Privacy",
    y="Utility",
    z="Safety",
    color="Safety",   # still show safety as color
    text="Paper",
    color_continuous_scale=[
    [0.0, "#B2182B"],   # bad safety = dark red
    [0.3, "#EF8A62"],   # low-medium = orange
    [0.6, "#FEE08B"],   # medium = yellow
    [0.8, "#A6D96A"],   # good = light green
    [1.0, "#1A9850"],   # best safety = green
    ]
)


fig.update_traces(textfont=dict(size=10, color="black")) 
fig.update_layout(
    scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)), 
    font=dict(size=15),
    scene=dict(
        xaxis_title="Privacy",
        yaxis_title="Utility",
        zaxis_title="Safety"

    )
)
fig.update_coloraxes(colorbar_title="Safety")

fig.show()
