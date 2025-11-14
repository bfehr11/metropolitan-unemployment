import streamlit as st
import pandas as pd
import json
import plotly.express as px

data = json.load(open('bls_unemployment.json'))
data = pd.DataFrame(data['Results']['series'][0]['data'])
data['periodName'] = data['periodName'] + " " + data['year']
data = data[::-1]

fig = px.line(data, x="periodName", y="value", title="The Unemployment Rate over the Years"
              , labels={'periodName': "", 'value': "Unemployment Rate"})
fig.show()
