import streamlit as st
import pandas as pd
import json
import plotly.express as px

nonfarm_employment = json.load(open('bls_nonfarm_employment.json'))
nonfarm_employment = pd.DataFrame(nonfarm_employment['Results']['series'][0]['data'])
current_nonfarm_employment = nonfarm_employment.iloc[0]

total_employment = json.load(open('bls_total_employment.json'))
total_employment = pd.DataFrame(total_employment['Results']['series'][0]['data'])
current_total_employment = total_employment.iloc[0]

total_unemployment = json.load(open('bls_total_unemployment.json'))
total_unemployment = pd.DataFrame(total_unemployment['Results']['series'][0]['data'])
current_total_unemployment = total_unemployment.iloc[0]

unemployment_rates = json.load(open('bls_unemployment_rates.json'))
unemployment_rates = pd.DataFrame(unemployment_rates['Results']['series'][0]['data'])
current_unemployment_rate = unemployment_rates.iloc[0]

st.title("Nationwide Employment (as of " + current_unemployment_rate['periodName'] + " " + current_unemployment_rate['year'] + ")")
st.write("Total non-farm employment (in thousands): " + current_nonfarm_employment['value'])
st.write("Total employment (in thousands): " + current_total_employment['value'])
st.write("Total unemployment (in thousands): " + current_total_unemployment['value'])
st.write("Unemployment rate: " + current_unemployment_rate['value'] + "%")

unemployment_rates['periodName'] = unemployment_rates['periodName'] + ", " + unemployment_rates['year']
unemployment_rates = unemployment_rates.loc[::-1]
fig = px.line(unemployment_rates, x="periodName", y="value", title="The Unemployment Rate over the Years"
              , labels={'periodName': "", 'value': "Unemployment Rate"})
st.plotly_chart(fig, use_container_width=True)
