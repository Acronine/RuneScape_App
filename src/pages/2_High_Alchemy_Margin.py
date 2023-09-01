import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

st.set_page_config(
    page_title="High Alchemy Margins",
    page_icon="⚔",
    menu_items={
        "About": """This app was made using the RuneScape Wiki
        Api. If you have any comments or run into any issues, here
        is my github: \n\rhttps://github.com/Acronine
        \n\rHigh Alchemy Profit is calculated by taking the gold return on
            casting high alchemy on the item, and subtracting the item's
            Grand Exchange price and subtracting 1 nature rune's Grand
            Exchange price."""
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
# This will auto play the selected song
c.autoplay_audio(r'src/Cellar_Song.ogg')
# Initial table to display the current price of a nature rune to give the user
#   a better understanding of the profit calculation
col1, col2 = st.columns(2)
with col1:
    st.data_editor(
            pd.DataFrame({"Nature Rune": [r"https://oldschool.runescape.wiki/images/Nature_rune.png"],
                         "Current GE Price": c.ha_price}),
            column_config={
                "Nature Rune": st.column_config.ImageColumn(
                    "Nature Rune", help="Shows the price for nature runes!"
                    )
                }, hide_index=True
    )
# Queries all the items that have actually been sold recently.
c.cdf = c.cdf[c.cdf["ge_price"] != 0]
# Sorting the values by the High Alchemy Profit to see top payouts.
c.cdf.sort_values(by="ha_profit",
                  ascending=False,
                  inplace=True)
c.cdf.reset_index(drop=True, inplace=True)
# Slider to select the top (#) of profitable items.
with col2:
    number_shown = st.select_slider(
        'Select the number of items you want displayed',
        options=[10,25,50]
        )
# Using the head option and sort values, we can easily pull the top items.
df = c.cdf.head(number_shown)
# Once the RuneScape Engine Class was initiated, the max profit can be
#   calculated. Creating a list of the values in order to be then added into
#   the Streamlit created data frame.
max_profit = [p*l for p, l in zip(df.ha_profit.tolist(), df.limit.tolist())]
# Creating a data frame to be displayed to the user. The column config is
#   allow Streamlit to display the images in the column. To force the data
#   frame to not have a scroll bar, a calculation was made to properly
#   stretch the height accordingly. Each row is about 35 pixels and the
#   column names' bar is 45 pixels.
st.data_editor({
    "Icon": df.icon.tolist(),
    "Item Name": df.name.tolist(),
    "GE Price": df.ge_price.tolist(),
    "H/A Return": df.highalch.tolist(),
    "H/Alch Profit": df.ha_profit.tolist(),
    'Limit': df.limit.tolist(),
    "Max Profit": max_profit,
    "Members": df.members.tolist()
    }, column_config={
        "Icon": st.column_config.ImageColumn(
            "Icon", help="Shows the price for nature runes!"
            ),
        "Members": st.column_config.ImageColumn(
            "Members", help="Shows the price for nature runes!"
            )
        }, hide_index=True, width=1000, height=(number_shown*35)+45
    )