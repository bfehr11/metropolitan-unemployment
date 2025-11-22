import streamlit as st
import pandas as pd

data = pd.read_csv("bls_metro_unemployment_rates.csv")

st.title("Change in Unemployment Rate")
period_length = st.sidebar.radio("Over the last _______"
                               , ['1 month', '6 months', '1 year', '5 years'])
rate_type = st.sidebar.radio("Type"
                             , ['monthly', 'annualized', 'total'])

rates = None
if period_length == "1 month":
    rates = pd.concat([data['city'], data.iloc[:, 4] - data.iloc[:, 3]], axis=1)
    rates.rename(columns={rates.columns[1]: 'Rate Change'}, inplace=True)
    if rate_type == "monthly":
        pass
    elif rate_type == "annualized":
        rates['Rate Change'] = 12*rates['Rate Change']
    elif rate_type == "total": 
        pass
elif period_length == "6 months":
    rates = pd.concat([data['city'], data.iloc[:, 9] - data.iloc[:, 3]], axis=1)
    rates.rename(columns={rates.columns[1]: 'Rate Change'}, inplace=True)
    if rate_type == "monthly":
        rates['Rate Change'] = rates['Rate Change'] / 6
    elif rate_type == "annualized":
        rates['Rate Change'] = 2*rates['Rate Change']
    elif rate_type == "total": 
        pass
elif period_length == "1 year":
    rates = pd.concat([data['city'], data.iloc[:, 15] - data.iloc[:, 3]], axis=1)
    rates.rename(columns={rates.columns[1]: 'Rate Change'}, inplace=True)
    if rate_type == "monthly":
        rates['Rate Change'] = rates['Rate Change'] / 12
    elif rate_type == "annualized":
        pass
    elif rate_type == "total": 
        pass
elif period_length == "5 years":
    rates = pd.concat([data['city'], data.iloc[:, 63] - data.iloc[:, 3]], axis=1)
    rates.rename(columns={rates.columns[1]: 'Rate Change'}, inplace=True)
    if rate_type == "monthly":
        rates['Rate Change'] = rates['Rate Change'] / 60
    elif rate_type == "annualized":
        rates['Rate Change'] = rates['Rate Change'] / 5
    elif rate_type == "total": 
        pass

rates.rename(columns={'city': 'City'}, inplace=True)
rates = rates.sort_values(by='Rate Change', ascending=False).reset_index(drop=True)
st.dataframe(rates.head(20), hide_index=True)