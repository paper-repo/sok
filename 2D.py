import pandas as pd
import plotly.express as px

df = pd.read_excel("scores.xlsx")
manual = {
    "4":      "bottom right",
    "18":      "middle left",
    "12":      "bottom right",
    "53":      "bottom left",
    "74":      "bottom left",


positions = [manual.get(str(p), "top center") for p in df["Paper"]]  

for p, pos in zip(df["Paper"], positions):
    if pos != "top center":
        print(f"  paper {p!r}  -> {pos}")
        
fig = px.scatter(
    df,
    x="Privacy",
    y="Utility",
    size=df["Safety"] + 0.05,        # +0.05 so S=0 papers are still visible as small dots
    color="Safety",
    text="Paper",
    range_x=[-0.02, 1.20],
    range_y=[-0.02, 1.20],
    range_color=[0, 1],
    color_continuous_scale=[
    [0.0, "#B2182B"],   # bad safety = dark red
    [0.3, "#EF8A62"],   # low-medium = orange
    [0.6, "#FEE08B"],   # medium = yellow
    [0.8, "#A6D96A"],   # good = light green
    [1.0, "#1A9850"],   # best safety = green
],
    size_max=28,
)

fig.update_traces(cliponaxis=False, 
                textposition=positions, 
                textfont=dict(size=10, color="black"), 
                hovertemplate=(
                                "<b>Paper: %{text}</b><br>"\
                                "Privacy: %{x:.2f}<br>"
                                "Utility: %{y:.2f}<br>"
                                "Safety: %{marker.color:.2f}"
                                "<extra></extra>"
                                ),
                )
fig.update_layout(
    xaxis_title="Privacy",
    yaxis_title="Utility",
    template="simple_white",
    width=700,
    height=600,
    margin=dict(l=60, r=20, b=60, t=20),
    coloraxis_colorbar=dict(
        title="Safety",
        tickvals=[0, 0.25, 0.5, 0.75, 1.0],
        ticktext=["Bad", "Low", "Medium", "Good", "Best"]
    )
)

fig.show()
