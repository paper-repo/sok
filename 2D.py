import pandas as pd
import plotly.express as px

df = pd.read_excel("scores.xlsx")
manual = {
    "2":      "bottom right",
    "19":      "middle left",
    "74":      "bottom right",
    "64":      "bottom left",
    "36":      "middle left",
    "44":      "bottom left",
    "45":      "bottom left"
}

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

# Find the row for Paper 70
target_paper = "70"

row = df[df["Paper"].astype(str) == target_paper].iloc[0]

x0 = row["Privacy"]
y0 = row["Utility"]
s0 = row["Safety"]

fig.add_annotation(
    x=x0,
    y=y0,
    text=(
        f"<b>Paper: {target_paper}</b><br>"
        f"Privacy: {x0:.2f}<br>"
        f"Utility: {y0:.2f}<br>"
        f"Safety: {s0:.2f}"
    ),
    showarrow=False,
    xanchor="left",
    yanchor="bottom",
    xshift=10,
    yshift=10,
    align="left",
    bgcolor="#B2182B",      
    bordercolor="#B2182B",
    borderwidth=1,
    font=dict(color="white", size=12),
    opacity=0.95
)

fig.write_image(
    "plot_with_hover_label.png",
    width=700,
    height=600,   
    scale=1       
)

fig.show()
