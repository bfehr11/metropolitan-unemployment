import requests
import time
import json
import os
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

metro_series_ids = {
    "New York, NY": ["LAUMT363562000000003", "Mid-Atlantic North"],
    "Los Angeles, CA": ["LAUMT063108000000003", "West Coast"],
    "Chicago, IL": ["LAUMT171698000000003", "Great Lakes"], 
    "Houston, TX": ["LAUMT482642000000003", "Gulf Coast"],
    "Phoenix, AZ": ["LAUMT043806000000003", "Southwest"],
    "Philadelphia, PA": ["LAUMT423798000000003", "Mid-Atlantic North"],
    "San Antonio, TX": ["LAUMT484170000000003", "Southwest"],
    "San Diego, CA": ["LAUMT064174000000003", "West Coast"],
    "Dallas, TX": ["LAUMT481910000000003", "Great Plains"],
    "Jacksonville, FL": ["LAUMT122726000000003", "Deep South"], 
    "San Jose, CA": ["LAUMT064194000000003", "West Coast"],
    "Austin, TX": ["LAUMT481242000000003", "Great Plains"],
    "Charlotte, NC": ["LAUMT371674000000003", "South"],
    "Columbus, OH": ["LAUMT391814000000003", "Heartland"],
    "Indianapolis, IN": ["LAUMT182690000000003", "Heartland"],
    "San Francisco, CA": ["LAUMT064186000000003", "West Coast"], 
    "Seattle, WA": ["LAUMT534266000000003", "Northwest"], 
    "Denver, CO": ["LAUMT081974000000003", "Mountain West"],
    "Oklahoma City, OK": ["LAUMT403642000000003", "Great Plains"],
    "Nashville, TN": ["LAUMT473498000000003", "Appohzarka"],
    "Washington, DC": ["LAUMT114790000000003", "Mid-Atlantic North"],
    "El Paso, TX": ["LAUMT482134000000003", "Southwest"],
    "Las Vegas, NV": ["LAUMT322982000000003", "Southwest"],
    "Boston, MA": ["LAUMT251446000000003", "Northeast"], 
    "Detroit, MI": ["LAUMT261982000000003", "Great Lakes"],
    "Louisville, KY": ["LAUMT213114000000003", "Appohzarka"],
    "Portland, OR": ["LAUMT413890000000003", "Northwest"],
    "Memphis, TN": ["LAUMT473282000000003", "Appohzarka"],
    "Baltimore, MD": ["LAUMT241258000000003", "Mid-Atlantic North"],
    "Milwaukee, WI": ["LAUMT553334000000003", "Great Lakes"], 
    "Albuquerque, NM": ["LAUMT351074000000003", "Southwest"],
    "Tucson, AZ": ["LAUMT044606000000003", "Southwest"],
    "Fresno, CA": ["LAUMT062342000000003", "West Coast"], 
    "Sacramento, CA": ["LAUMT064090000000003", "West Coast"], 
    "Atlanta, GA": ["LAUMT131206000000003", "Deep South"], 
    "Kansas City, MO": ["LAUMT292814000000003", "Heartland"],
    "Raleigh, NC": ["LAUMT373958000000003", "Mid-Atlantic South"],
    "Colorado Springs, CO": ["LAUMT081782000000003", "Mountain West"],
    "Omaha, NE": ["LAUMT313654000000003", "Heartland"],
    "Miami, FL": ["LAUMT123310000000003", "Southern Florida"],
    "Virginia Beach, VA": ["LAUMT514726000000003", "Mid-Atlantic South"], 
    "Minneapolis, MN": ["LAUMT273346000000003", "Heartland"], 
    "Bakersfield, CA": ["LAUMT061254000000003", "West Coast"], 
    "Tulsa, OK": ["LAUMT404614000000003", "Great Plains"],
    "Tampa, FL": ["LAUMT124530000000003", "Southern Florida"],
    "Wichita, KS": ["LAUMT204862000000003", "Great Plains"],
    "Cleveland, OH": ["LAUMT391741000000003", "Heartland"],
    "New Orleans, LA": ["LAUMT223538000000003", "Gulf Coast"],
    "Honolulu, HI": ["LAUMT154652000000003", "West Coast"],
    "Orlando, FL": ["LAUMT123674000000003", "Southern Florida"]
}

data = pd.DataFrame(columns = [None] * 238)
curr_year = datetime.now().year

def call_bls(series_id):
    payload = { 
        "seriesid": [series_id],
        "startyear": str(curr_year - 19),
        "endyear": str(curr_year), 
        "registrationkey": "526215c8390e4569998f80cc40898dcf"
    }
    response = requests.post(BLS_API, json=payload)
    response.raise_for_status()
    data = response.json()
    return data

for key, value in metro_series_ids.items():
    series_data = call_bls(value[0])
    temp = pd.DataFrame(series_data['Results']['series'][0]['data'])
    if len(data) == 0:
        data.columns = pd.concat([pd.Series(["city"]), pd.Series(["Region"]), (temp['periodName'] + ", " + temp['year'])])
    
    new_row = [key, value[1]] + [None] * (236 - len(temp)) + temp['value'].values.tolist()
    new_row = pd.DataFrame([new_row], columns=data.columns)

    data = pd.concat([data, new_row], ignore_index=True)

geolocator = Nominatim(user_agent="st-us-cities")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
rows = []
for c in data["city"].dropna().unique():
    loc = geocode(f"{c}, USA") or geocode(c)
    rows.append((c, getattr(loc, "latitude", None), getattr(loc, "longitude", None)))
geo = pd.DataFrame(rows, columns=["city", "lat", "lon"])
data = data.merge(geo, on="city", how="left")

data.to_csv("bls_metro_unemployment_rates.csv")