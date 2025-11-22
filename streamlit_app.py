import streamlit as st
import pandas as pd

pages = {
    "Nationwide Statistics": [
        st.Page("nationwide_stats.py", title="What is Employment like Nationwide?")
    ],
    "Unemployment Rates Across the Country": [
        st.Page("unemployment_map.py", title="Map"),
    ],
    "Unemployment Trends": [
        st.Page("metro_unemployment_trends.py", title="Metros")
    ]
}

pg = st.navigation(pages, position="top")
pg.run()