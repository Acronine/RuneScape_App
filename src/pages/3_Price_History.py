import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
import requests, json
from datetime import datetime
st.set_page_config(
    page_title="Price History",
    page_icon="⚔"
    )

# Setting up the filepath to allow the app to pull from the directory.
filepath = os.path.join(Path(__file__).parents[1])
sys.path.insert(0, filepath)

# Importing RuneScapeEngine
from runescape_query_engine import RuneScapeEngine
# Initiating the RuneScapeEngine to pull from MongoDB and query
#  the latest information on the Grand Exchange Prices
c = RuneScapeEngine()

c.autoplay_audio(r'src/Harmony.ogg')

df = c.cdf[c.cdf["ge_price"] != 0]
df.reset_index(drop=True, inplace=True)

price_list = df.name.tolist()

select = st.selectbox(
    'Search to see the price of any Item on the Grand Exchange over a set time.',
    options=price_list
    )

time_frame = st.select_slider(
    'Select the increments of time you want to see.',
    options=["5m", "1h", "6h", "24h"]
    )
time_start, time_end = st.select_slider(
    'Select the range of time you want to view.',
    options=range(1,366),
    value=(1,365)
    )
split_check = True
if st.button("Split or Join Graphs"):
    if split_check == True:
        split_check = False
    elif split_check == False:
        split_check = True


item_frame = df[df['name'] == select].reset_index()
info = requests.get(
    fr"""https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep={time_frame}&id={item_frame['id'][0]}""",
    headers=c.header_price
    ).json()
avg_high = []
avg_low = []
timing = []
for i in range(len(info["data"])):
    if info["data"][i]["avgHighPrice"] is None:
        try:
            avg_high.append(avg_high[i-1])
        except:
            for e in range(len(info["data"])):
                if info["data"][e]["avgHighPrice"] is not None:
                    avg_high.append(info["data"][e]["avgHighPrice"])
                    break
    else:
        avg_high.append(info["data"][i]["avgHighPrice"])
    if info["data"][i]["avgLowPrice"] is None:
        try:
            avg_low.append(avg_low[i-1])
        except:
            for e in range(len(info["data"])):
                if info["data"][e]["avgLowPrice"] is not None:
                    avg_low.append(info["data"][e]["avgLowPrice"])
                    break
    else:
        avg_low.append(info["data"][i]["avgLowPrice"])
    stamp = datetime.utcfromtimestamp(info["data"][i]['timestamp'])
    timing.append(stamp.strftime('%d %b %Y - %H:%M'))
prices = pd.DataFrame({
    "Average High Price": avg_high,
    "Average Low Price": avg_low,
    "Time": timing
}
)
st.subheader(select)
if split_check == True:
    st.line_chart(
        data=prices[time_start-1: time_end-1],
        x = 'Time',
        y = ["Average High Price", "Average Low Price"]
    )
elif split_check == False:
    st.line_chart(
        data=prices[time_start-1: time_end-1],
        x = 'Time',
        y = "Average High Price"
    )
    st.line_chart(
        data=prices[time_start-1: time_end-1],
        x = 'Time',
        y = "Average Low Price"
    )
