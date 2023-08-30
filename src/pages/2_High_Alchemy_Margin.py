import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

st.set_page_config(
    page_title="High Alchemy Margins",
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

c.autoplay_audio(r'data/Cellar_Song.ogg')

st.data_editor(
        pd.DataFrame({"Nature Rune": [r"https://oldschool.runescape.wiki/images/Nature_rune.png"],
                      "Current GE Price": c.ha_price}),
        column_config={
            "Nature Rune": st.column_config.ImageColumn(
                "Nature Rune", help="Shows the price for nature runes!"
                )
            }, hide_index=True
)
c.cdf = c.cdf[c.cdf["ge_price"] != 0]
c.cdf.sort_values(by="ha_profit",
                  ascending=False,
                  inplace=True)
c.cdf.reset_index(drop=True, inplace=True)

number_shown = st.select_slider(
    'Select the number of items you want displayed',
    options=[10,25,50]
    )
df = c.cdf.head(number_shown)
max_profit = [p*l for p, l in zip(df.ha_profit.tolist(), df.limit.tolist())]
st.data_editor({
    "Icon": df.icon.tolist(),
    "Item Name": df.name.tolist(),
    "GE Price": df.ge_price.tolist(),
    "H/A Return": df.highalch.tolist(),
    "H/Alch Profit": df.ha_profit.tolist(),
    'Limit': df.limit.tolist(),
    "Max Profit": max_profit,
    "Members": df.members.tolist()
    },column_config={
        "Icon": st.column_config.ImageColumn(
            "Icon", help="Shows the price for nature runes!"
            ),
        "Members": st.column_config.ImageColumn(
            "Members", help="Shows the price for nature runes!"
            )
        }, hide_index=True, width=1000, height=(number_shown*35)+45)