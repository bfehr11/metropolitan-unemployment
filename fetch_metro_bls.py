import requests
import time
import json
import os
import pandas as pd

BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

metro_series_ids = {
    "New York, NY": "LAUMT363562000000003",
    "Los Angeles, CA": "LAUMT063108000000003",
    "Chicago, IL": "LAUMT171698000000003", 
    "Houston, TX": "LAUMT482642000000003",
    "Phoenix, AZ": "LAUMT043806000000003", 
    "Philadelphia, PA": "LAUMT423798000000003",
    "San Antonio, TX": "LAUMT484170000000003", 
    "San Diego, CA": "LAUMT064174000000003",
    "Dallas, TX": "LAUMT481910000000003",
    "Jacksonville, FL": "LAUMT122726000000003", 
    "San Jose, CA": "LAUMT064194000000003", 
    "Austin, TX": "LAUMT481242000000003", 
    "Charlotte, NC": "LAUMT371674000000003", 
    "Columbus, OH": "LAUMT391814000000003", 
    "Indianapolis, IN": "LAUMT182690000000003", 
    "San Francisco, CA": "LAUMT064186000000003", 
    "Seattle, WA": "LAUMT534266000000003", 
    "Denver, CO": "LAUMT081974000000003", 
    "Oklahoma City, OK": "LAUMT403642000000003",
    "Nashville, TN": "LAUMT473498000000003",
    "Washington, DC": "LAUMT114790000000003", 
    "El Paso, TX": "LAUMT482134000000003", 
    "Las Vegas, NV": "LAUMT322982000000003",
    "Boston, MA": "LAUMT251446000000003", 
    "Detroit, MI": "LAUMT261982000000003",
    "Louisville, KY": "LAUMT213114000000003", 
    "Portland, OR": "LAUMT413890000000003",
    "Memphis, TN": "LAUMT473282000000003", 
    "Baltimore, MD": "LAUMT241258000000003",
    "Milwaukee, WI": "LAUMT553334000000003", 
    "Albuquerque, NM": "LAUMT351074000000003",
    "Tucson, AZ": "LAUMT044606000000003",
    "Fresno, CA": "LAUMT062342000000003", 
    "Sacramento, CA": "LAUMT064090000000003",
    "Atlanta, GA": "LAUMT131206000000003", 
    "Kansas City, MO": "LAUMT292814000000003",
    "Raleigh, NC": "LAUMT373958000000003",
    "Colorado Springs, CO": "LAUMT081782000000003",
    "Omaha, NE": "LAUMT313654000000003",
    "Miami, FL": "LAUMT123310000000003",
    "Virginia Beach, VA": "LAUMT514726000000003", 
    "Minneapolis, MN": "LAUMT273346000000003", 
    "Bakersfield, CA": "LAUMT061254000000003", 
    "Tulsa, OK": "LAUMT404614000000003",
    "Tampa, FL": "LAUMT124530000000003",
    "Wichita, KS": "LAUMT204862000000003",
    "Cleveland, OH": "LAUMT391741000000003",
    "New Orleans, LA": "LAUMT223538000000003",
    "Honolulu, HI": "LAUMT154652000000003", 
    "Orlando, FL": "LAUMT123674000000003"
}

data = pd.DataFrame(columns = [None] * 240)

def call_bls(series_id):
    payload = { 
        "seriesid": [series_id],
        "startyear": "1990",
        "endyear": "9999", 
        "registrationkey": "054aebaf933d47399ceff04caf6e4a9b"
    }
    response = requests.post(BLS_API, json=payload)
    response.raise_for_status()
    data = response.json()
    return data

for key, value in metro_series_ids.items():
    series_data = call_bls(value)
    temp = pd.DataFrame(series_data['Results']['series'][0]['data'])
    if len(data) == 0:
        data.columns = temp['periodName'] + ", " + temp['year']
    
    new_row = [None] * (240 - len(temp)) + temp['value'].values.tolist()
    new_row = pd.DataFrame([new_row], columns=data.columns)

    data = pd.concat([data, new_row], ignore_index=True)

data.to_csv("bls_metro_unemployment_rates.csv")
