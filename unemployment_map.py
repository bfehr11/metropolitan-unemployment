# app.py
import pandas as pd
import streamlit as st
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

st.set_page_config(page_title="US City Dots", layout="wide")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.drop(columns=[df.columns[0]])           # drop index column
    df = df.rename(columns={df.columns[0]: "city", df.columns[1]: "value"})
    return df[["city", "value"]]

@st.cache_data
def geocode_cities(cities: pd.Series) -> pd.DataFrame:
    geolocator = Nominatim(user_agent="st-us-cities")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    rows = []
    for c in cities.dropna().unique():
        loc = geocode(f"{c}, USA") or geocode(c)
        rows.append((c, getattr(loc, "latitude", None), getattr(loc, "longitude", None)))
    return pd.DataFrame(rows, columns=["city", "lat", "lon"])

def main():
    df = load_data("bls_metro_unemployment_rates.csv")
    geo = geocode_cities(df["city"])
    m = df.merge(geo, on="city", how="left").dropna(subset=["lat", "lon"])

    fig = px.scatter_mapbox(
        m,
        lat="lat",
        lon="lon",
        size="value",
        size_max=30,
        hover_name="city",
        hover_data={"value": True, "lat": False, "lon": False},
        zoom=3,
        center={"lat": m["lat"].mean(), "lon": m["lon"].mean()},
        height=700,
    )
    fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=30, b=0))

    st.title("US Cities — Sized by Value")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()