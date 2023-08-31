import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
import requests, json
from datetime import datetime

st.set_page_config(
    page_title="Price History",
    page_icon="⚔",
    menu_items={
        "About": """This app was made using the RuneScape Wiki
        Api. If you have any comments or run into any issues, here
        is my github: \n\rhttps://github.com/Acronine"""
    }
    )

# Setting up the filepath to allow the app to pull from the directory.
filepath = os.path.join(Path(__file__).parents[1])
sys.path.insert(0, filepath)

# Importing RuneScapeEngine
from runescape_query_engine import RuneScapeEngine
# Initiating the RuneScapeEngine to pull from MongoDB and query
#  the latest information on the Grand Exchange Prices
c = RuneScapeEngine()
# This function autoplays the selected music.
c.autoplay_audio(r'src/Harmony.ogg')

# Queries all the items that have actually been sold recently.
df = c.cdf[c.cdf["ge_price"] != 0]
df.reset_index(drop=True, inplace=True)

# Creating a list of names to be used as options for the select box.
price_list = df.name.tolist()
select = st.selectbox(
    'Search to see the price of any Item on the Grand Exchange over set time.',
    options=price_list
    )

# Slider allows user to pick what 365 increments of time they want to see.
time_frame = st.select_slider(
    label=("""Select the increments of time you want to see. Your options are:
            5 minutes, 1 hour, 6 hours, and 24 hours."""),
    options=["5m", "1h", "6h", "24h"]
    )
# Slider allows the user to look at a specific range of the increments they
#   would like to see. The range starts at 1 for the user's benefit.
#   When applying it into code, it will be subtracted by 1 to correct it.
time_start, time_end = st.select_slider(
    f'Select the range of {time_frame} increments you want to view.',
    options=range(1, 366),
    value=(1, 365)
    )
# Sets the single row of the data frame with that name & deletes the index.
item_frame = df[df['name'] == select].reset_index()
# With the information given, queries the data directly and stores into
#   a variable.
info = requests.get(
    fr"""https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep={time_frame}&id={item_frame['id'][0]}""",
    headers=c.header_price
    ).json()
# Creating three empty lists to use as the columns for each data category.
avg_high = []
avg_low = []
timing = []
# Looping through all 365 intervals and adding the current price into the
#   corresponding lists. In case if no item was sold during that interval,
#   it's normally set to null. The loop will just add the previous price
#   in its stead. In the case of the first interval being null, a new loop
#   will go through until it hits an interval with a price, and sets that as
#   the first price.
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
    # This is to convert the time from Unix to date format for readability.
    stamp = datetime.utcfromtimestamp(info["data"][i]['timestamp'])
    timing.append(stamp.strftime('%d %b %Y - %H:%M'))
# Setting the now filled lists into a data frame for the chart.
prices = pd.DataFrame({
    "Average High Price": avg_high,
    "Average Low Price": avg_low,
    "Time": timing
    }
                      )
# Created a toggle button to allow the user to split the two averages lines.
pushed = st.toggle("Split the Graphs?")
# Displays the item's name.
st.subheader(select)
# Setting an if statement on the toggle to either display one combined graph,
#   or two separate graphs.
if pushed == False:
    st.line_chart(
        data=prices[time_start-1: time_end-1],
        x='Time',
        y=["Average High Price", "Average Low Price"],
        width=800
    )
elif pushed == True:
    st.line_chart(
        data=prices[time_start-1: time_end-1],
        x='Time',
        y="Average High Price",
        width=800
    )
    st.line_chart(
        data=prices[time_start-1: time_end-1],
        x='Time',
        y="Average Low Price",
        width=800
    )
