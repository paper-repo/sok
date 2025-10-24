import plotly.express as px
import pandas as pd

df = pd.read_excel("scores.xlsx", engine="openpyxl")

fig = px.scatter_3d(
    df,
    x="Privacy", y="Utility", z="Safety",
    color="Safety", text="Paper"
)
fig.update_layout(
    font=dict(
        family="Nimbus Roman No9 L",  
        size=14,
        color="black"
    ),
    scene=dict(
        xaxis=dict(
            title=dict(
                text="Privacy",
                font=dict(family="Nimbus Roman No9 L", size=30, color="black")  
            )
        ),
        yaxis=dict(
            title=dict(
                text="Utility",
                font=dict(family="Nimbus Roman No9 L", size=30, color="black")  
            )
        ),
        zaxis=dict(
            title=dict(
                text="Safety",
                font=dict(family="Nimbus Roman No9 L", size=30, color="black")  
            )
        )
    )
)

fig.update_traces(
    hovertemplate="<b>Privacy</b>=%{x}<br><b>Utility</b>=%{y}<br><b>Safety</b>=%{z}<br><b>Paper</b>=%{text}",
    hoverlabel=dict(
        font_size=30,
        font_family="Nimbus Roman No9 L",  
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="black"
    )
)

fig.update_coloraxes(colorbar_title="Range")

fig.show()
