import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# get data, drop index column, and rename columns
data = pd.read_csv("bls_metro_unemployment_rates.csv")
data = data.drop(columns=[data.columns[0]])
data = data.rename(columns={data.columns[0]: "city", data.columns[2]: "value"})[["city", "value", "lat", "lon"]]

# scale unemployment rate to allow for differences to be seen better
vmin = data["value"].min()
vmax = data["value"].max()
data["size"] = np.interp(data["value"], (vmin, vmax), (8, 60))

fig = px.scatter_mapbox(
    data,
    lat="lat",
    lon="lon",
    hover_name="city",
    hover_data={"value": ":.2f", "lat": False, "lon": False},
    zoom=3,
    center={"lat": data["lat"].mean(), "lon": data["lon"].mean()}, # center map on the United States
    height=700,
)
fig.update_traces(marker=dict(size=data["size"].tolist()))
fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=30, b=0))

st.title("Current Metro Unemployment Rates")
st.plotly_chart(fig, use_container_width=True)