import plotly.graph_objects as go
from plotly import data
import streamlit as st
import numpy as np
import plotly.figure_factory as ff

df = data.tips()[data.tips()["day"] == "Sun"]

mean_values_df = df.groupby(by=["sex", "smoker"], as_index=False).mean(
    numeric_only=True
)

smoker_mean = mean_values_df[mean_values_df.smoker == "Yes"].sort_values(
    by="tip", ascending=False
)
non_smoker_mean = mean_values_df[mean_values_df.smoker == "No"].sort_values(
    by="tip", ascending=False
)

smoker = df[df.smoker == "Yes"].sort_values(by="tip", ascending=False)
non_smoker = df[df.smoker == "No"].sort_values(by="tip", ascending=False)

fig = go.Figure(
    layout=dict(
        xaxis=dict(categoryorder="category descending"),
        yaxis=dict(range=[0, 7]),
        scattermode="group",
        legend=dict(groupclick="toggleitem"),
    )
)

fig.add_trace(
    go.Bar(
        x=smoker_mean.sex,
        y=smoker_mean.tip,
        name="Average",
        marker_color="IndianRed",
        offsetgroup="smoker",
        legendgroup="smoker",
        legendgrouptitle_text="Smoker",
    )
)


fig.add_trace(
    go.Scatter(
        x=smoker.sex,
        y=smoker.tip,
        mode="markers",
        name="Individual tips",
        marker=dict(color="LightSlateGrey", size=5),
        offsetgroup="smoker",
        legendgroup="smoker",
    )
)

fig.add_trace(
    go.Bar(
        x=non_smoker_mean.sex,
        y=non_smoker_mean.tip,
        name="Average",
        marker_color="LightSalmon",
        offsetgroup="non-smoker",
        legendgroup="non-smoker",
        legendgrouptitle_text="Non-Smoker",
    )
)


fig.add_trace(
    go.Scatter(
        x=non_smoker.sex,
        y=non_smoker.tip,
        mode="markers",
        name="Individual tips",
        marker=dict(color="LightSteelBlue", size=5),
        offsetgroup="non-smoker",
        legendgroup="non-smoker",
    )
)

#fig.show()

# Plot!
st.plotly_chart(fig, use_container_width=True,theme="streamlit")