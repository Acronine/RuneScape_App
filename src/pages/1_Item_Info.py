import streamlit as st
import os
import sys
from pathlib import Path
import pandas as pd

st.set_page_config(
    page_title="Item Info",
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

c.autoplay_audio(r'src/Background(1).ogg')

# Creating a list of names to be used as options for the select box.
geit_list = c.cdf.name.tolist()
select = st.selectbox(
    'Search any Item on the Grand Exchange',
    options=geit_list
    )

if select:
    # Displays the name of the item selected.
    st.subheader(select)
    # Sets the single row of the data frame with that name & deletes the index.
    item_frame = c.cdf[c.cdf['name'] == select].reset_index()
    # Storing item id in a variable to avoid repetitive typing.
    item_id = int(item_frame['id'][0])

    # Displaying an image using the url and icon value from the data frame.
    # This also displays the description under the image as a caption.
    st.image(f"{item_frame['icon'][0]}", width=180,
             caption=item_frame['description'][0])

    ge_value = int(item_frame['ge_price'][0])
    # Streamlit auto adds commas to integers, converting back removes them.
    ha_value = int(item_frame["highalch"][0])
    # This is the equation for high alchemy profit
    hap_py = int(item_frame["ha_profit"][0])
    # Creating initial table for membership icon and item id.
    st.data_editor(
        pd.DataFrame({"Members": [item_frame["members"][0]], "Item Id": f"{item_id}"}),
        column_config={
            "Members": st.column_config.ImageColumn(
                "Membership only?", help="Members only item"
                )
            },
        hide_index=True
    )

    # Creating a second table that will display all relevant prices.
    st.dataframe(
        {
            "Current Ge Price": f"{ge_value} gp",
            "Price in $USD": f"${item_frame['usd_value'][0]}",
            "High Alchemy Profit": f"{(hap_py)} gp",
            "Vendor Price": f"{item_frame['gp_value'][0]} gp",
            "High Alch Return": f"{ha_value} gp",
            "Low Alch Return": f"{item_frame['lowalch'][0]} gp",
            "Buy Limit": f"{item_frame['limit'][0]}"
        }, width=800
    )
    # This will check if there is profit to be made. it will tell the user
    # in a sentence the amount you would get buying the full limit and casting
    # high alchemy on each item.
    if (hap_py > 0) & (item_frame['limit'][0] > 0):
        st.markdown(f"""If you were to buy {item_frame['limit'][0]} {select}
                    and cast high alchemy on each item, 
                    you would make {hap_py * item_frame['limit'][0]} gp.""")
